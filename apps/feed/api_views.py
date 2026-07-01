from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from .models import Atividade
from apps.usuarios.serializers import UsuarioSerializer
from apps.destinos.serializers import DestinoListSerializer


class AtividadeSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    destino = DestinoListSerializer(read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)

    class Meta:
        model = Atividade
        fields = ['id', 'usuario', 'tipo', 'tipo_display', 'destino', 'grupo', 'created_at']


class FeedView(generics.ListAPIView):
    serializer_class = AtividadeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        seguindo_ids = self.request.user.seguindo.values_list('id', flat=True)
        return Atividade.objects.filter(
            usuario_id__in=seguindo_ids
        ).select_related('usuario', 'destino', 'grupo')[:50]
