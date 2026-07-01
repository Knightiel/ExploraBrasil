from django.db import models
from django.conf import settings


class GrupoExpedicao(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(null=True, blank=True)
    destino = models.ForeignKey('destinos.Destino', on_delete=models.CASCADE, related_name='grupos')
    criador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='grupos_criados')
    membros = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='grupos_participando', blank=True)
    data_expedicao = models.DateTimeField(null=True, blank=True)
    vagas = models.PositiveSmallIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Grupo de Expedição'
        verbose_name_plural = 'Grupos de Expedição'
        ordering = ['-created_at']

    def __str__(self):
        return self.nome

    @property
    def total_membros(self):
        return self.membros.count()

    @property
    def vagas_disponiveis(self):
        return max(0, self.vagas - self.membros.count())


class PontoEncontro(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(null=True, blank=True)
    destino = models.ForeignKey('destinos.Destino', on_delete=models.CASCADE, related_name='pontos_encontro')
    grupo = models.ForeignKey(GrupoExpedicao, on_delete=models.SET_NULL, null=True, blank=True, related_name='pontos_encontro')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    criador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pontos_criados')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ponto de Encontro'
        verbose_name_plural = 'Pontos de Encontro'

    def __str__(self):
        return self.nome
