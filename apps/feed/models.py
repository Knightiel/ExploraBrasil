from django.db import models
from django.conf import settings


class Atividade(models.Model):
    TIPOS = [
        ('avaliou', 'Avaliou um destino'),
        ('comentou', 'Comentou em um destino'),
        ('entrou_grupo', 'Entrou em um grupo'),
        ('favoritou', 'Favoritou um destino'),
        ('cadastrou_destino', 'Cadastrou um destino'),
        ('criou_grupo', 'Criou um grupo de expedição'),
        ('seguiu', 'Passou a seguir'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='atividades')
    tipo = models.CharField(max_length=30, choices=TIPOS)
    destino = models.ForeignKey('destinos.Destino', on_delete=models.CASCADE, null=True, blank=True)
    grupo = models.ForeignKey('grupos.GrupoExpedicao', on_delete=models.CASCADE, null=True, blank=True)
    usuario_alvo = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='atividades_sobre')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'

    def __str__(self):
        return f'{self.usuario} {self.get_tipo_display()}'
