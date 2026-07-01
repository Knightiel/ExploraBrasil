from rest_framework import serializers
from .models import Comentario
from apps.usuarios.serializers import UsuarioSerializer


class ComentarioSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    respostas = serializers.SerializerMethodField()

    class Meta:
        model = Comentario
        fields = ['id', 'texto', 'usuario', 'parent', 'respostas', 'created_at']
        read_only_fields = ['usuario', 'created_at']

    def get_respostas(self, obj):
        if obj.respostas.exists():
            return ComentarioSerializer(obj.respostas.all(), many=True).data
        return []
