from rest_framework import serializers
from .models import GrupoExpedicao, PontoEncontro
from apps.usuarios.serializers import UsuarioSerializer
from apps.destinos.serializers import DestinoListSerializer


class PontoEncontroSerializer(serializers.ModelSerializer):
    criador = UsuarioSerializer(read_only=True)

    class Meta:
        model = PontoEncontro
        fields = ['id', 'nome', 'descricao', 'latitude', 'longitude', 'criador', 'created_at']
        read_only_fields = ['criador', 'created_at']


class GrupoSerializer(serializers.ModelSerializer):
    criador = UsuarioSerializer(read_only=True)
    membros = UsuarioSerializer(many=True, read_only=True)
    destino = DestinoListSerializer(read_only=True)
    destino_id = serializers.PrimaryKeyRelatedField(
        queryset=__import__('apps.destinos.models', fromlist=['Destino']).Destino.objects.all(),
        source='destino', write_only=True
    )
    total_membros = serializers.ReadOnlyField()
    vagas_disponiveis = serializers.ReadOnlyField()
    pontos_encontro = PontoEncontroSerializer(many=True, read_only=True)

    class Meta:
        model = GrupoExpedicao
        fields = ['id', 'nome', 'descricao', 'destino', 'destino_id', 'criador',
                  'membros', 'data_expedicao', 'vagas', 'total_membros',
                  'vagas_disponiveis', 'pontos_encontro', 'created_at']
        read_only_fields = ['criador', 'created_at', 'membros']
