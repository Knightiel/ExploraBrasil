from rest_framework import serializers
from .models import Categoria, Destino, FotoDestino, Avaliacao, Favorito
from apps.usuarios.serializers import UsuarioSerializer


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class FotoDestinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoDestino
        fields = ['id', 'url', 'legenda', 'ordem']


class DestinoListSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    media_avaliacao = serializers.ReadOnlyField()
    total_avaliacoes = serializers.ReadOnlyField()
    foto_principal = serializers.ReadOnlyField()
    distancia = serializers.FloatField(read_only=True, default=None)

    class Meta:
        model = Destino
        fields = ['id', 'nome', 'descricao', 'latitude', 'longitude',
                  'dificuldade', 'categoria', 'foto_principal',
                  'media_avaliacao', 'total_avaliacoes', 'distancia']


class DestinoDetailSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), source='categoria', write_only=True, required=False
    )
    criador = UsuarioSerializer(read_only=True)
    fotos = FotoDestinoSerializer(many=True, read_only=True)
    media_avaliacao = serializers.ReadOnlyField()
    total_avaliacoes = serializers.ReadOnlyField()

    class Meta:
        model = Destino
        fields = ['id', 'nome', 'descricao', 'latitude', 'longitude',
                  'dificuldade', 'distancia_km', 'categoria', 'categoria_id',
                  'criador', 'aprovado', 'fotos', 'media_avaliacao',
                  'total_avaliacoes', 'created_at']
        read_only_fields = ['aprovado', 'criador', 'created_at']


class AvaliacaoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = Avaliacao
        fields = ['id', 'nota', 'usuario', 'created_at']
        read_only_fields = ['usuario', 'created_at']
