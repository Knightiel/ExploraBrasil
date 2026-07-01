from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Comentario
from .serializers import ComentarioSerializer
from apps.destinos.models import Destino
from apps.feed.models import Atividade


class ComentarioListCreateView(generics.ListCreateAPIView):
    serializer_class = ComentarioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comentario.objects.filter(
            destino_id=self.kwargs['destino_id'],
            parent__isnull=True
        ).select_related('usuario').prefetch_related('respostas__usuario')

    def perform_create(self, serializer):
        destino = Destino.objects.get(pk=self.kwargs['destino_id'])
        comentario = serializer.save(usuario=self.request.user, destino=destino)
        if not comentario.parent:
            Atividade.objects.create(usuario=self.request.user, tipo='comentou', destino=destino)


class ComentarioDeleteView(generics.DestroyAPIView):
    queryset = Comentario.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.usuario != request.user and not request.user.is_staff:
            return Response({'error': 'Sem permissão.'}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)
