from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import GrupoExpedicao, PontoEncontro
from .serializers import GrupoSerializer, PontoEncontroSerializer
from apps.feed.models import Atividade


class GrupoListCreateView(generics.ListCreateAPIView):
    serializer_class = GrupoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = GrupoExpedicao.objects.select_related('destino', 'criador').prefetch_related('membros')
        destino_id = self.request.query_params.get('destino')
        if destino_id:
            qs = qs.filter(destino_id=destino_id)
        return qs

    def perform_create(self, serializer):
        grupo = serializer.save(criador=self.request.user)
        grupo.membros.add(self.request.user)
        Atividade.objects.create(usuario=self.request.user, tipo='criou_grupo', grupo=grupo)


class GrupoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GrupoExpedicao.objects.all()
    serializer_class = GrupoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class EntrarGrupoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            grupo = GrupoExpedicao.objects.get(pk=pk)
        except GrupoExpedicao.DoesNotExist:
            return Response({'error': 'Grupo não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user in grupo.membros.all():
            grupo.membros.remove(request.user)
            return Response({'membro': False})

        if grupo.vagas_disponiveis == 0:
            return Response({'error': 'Grupo sem vagas disponíveis.'}, status=status.HTTP_400_BAD_REQUEST)

        grupo.membros.add(request.user)
        Atividade.objects.create(usuario=request.user, tipo='entrou_grupo', grupo=grupo)
        return Response({'membro': True})


class PontoEncontroCreateView(generics.CreateAPIView):
    serializer_class = PontoEncontroSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        grupo = GrupoExpedicao.objects.get(pk=self.kwargs['pk'])
        serializer.save(criador=self.request.user, grupo=grupo, destino=grupo.destino)
