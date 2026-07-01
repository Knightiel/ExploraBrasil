from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Destino, Categoria, Avaliacao, Favorito
from .serializers import DestinoListSerializer, DestinoDetailSerializer, AvaliacaoSerializer, CategoriaSerializer
from .utils import destinos_proximos
from apps.feed.models import Atividade


class CategoriaListView(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = []


class DestinoListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        return DestinoListSerializer

    def get_queryset(self):
        qs = Destino.objects.filter(aprovado=True).select_related('categoria', 'criador').prefetch_related('fotos', 'avaliacoes')
        categoria = self.request.query_params.get('categoria')
        dificuldade = self.request.query_params.get('dificuldade')
        search = self.request.query_params.get('search')
        if categoria:
            qs = qs.filter(categoria__nome=categoria)
        if dificuldade:
            qs = qs.filter(dificuldade=dificuldade)
        if search:
            qs = qs.filter(nome__icontains=search)
        return qs

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        raio = float(request.query_params.get('raio', 50))

        if lat and lon:
            ids_dist = destinos_proximos(qs, float(lat), float(lon), raio)
            id_to_dist = {item[0]: item[1] for item in ids_dist}
            qs = [d for d in qs if d.id in id_to_dist]
            for d in qs:
                d.distancia = round(id_to_dist[d.id], 1)
            qs.sort(key=lambda d: d.distancia)
        else:
            for d in qs:
                d.distancia = None

        serializer = DestinoListSerializer(qs, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        destino = serializer.save(criador=self.request.user, aprovado=False)
        Atividade.objects.create(usuario=self.request.user, tipo='cadastrou_destino', destino=destino)


class DestinoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Destino.objects.all()
    serializer_class = DestinoDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AvaliarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            destino = Destino.objects.get(pk=pk)
        except Destino.DoesNotExist:
            return Response({'error': 'Destino não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        nota = request.data.get('nota')
        if nota is None or not (1 <= int(nota) <= 5):
            return Response({'error': 'Nota deve ser entre 1 e 5.'}, status=status.HTTP_400_BAD_REQUEST)

        avaliacao, created = Avaliacao.objects.update_or_create(
            destino=destino, usuario=request.user,
            defaults={'nota': int(nota)}
        )
        if created:
            Atividade.objects.create(usuario=request.user, tipo='avaliou', destino=destino)
        return Response(AvaliacaoSerializer(avaliacao).data)


class FavoritarView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            destino = Destino.objects.get(pk=pk)
        except Destino.DoesNotExist:
            return Response({'error': 'Destino não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        fav, created = Favorito.objects.get_or_create(usuario=request.user, destino=destino)
        if not created:
            fav.delete()
            return Response({'favoritado': False})
        Atividade.objects.create(usuario=request.user, tipo='favoritou', destino=destino)
        return Response({'favoritado': True})
