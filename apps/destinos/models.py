from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Categoria(models.Model):
    TIPOS = [
        ('trilha', 'Trilha'),
        ('acampamento', 'Acampamento'),
        ('ponto_turistico', 'Ponto Turístico'),
    ]
    nome = models.CharField(max_length=100, choices=TIPOS, unique=True)
    icone = models.CharField(max_length=50, default='bi-geo-alt')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.get_nome_display()


class Destino(models.Model):
    DIFICULDADE = [
        ('facil', 'Fácil'),
        ('moderado', 'Moderado'),
        ('dificil', 'Difícil'),
    ]

    nome = models.CharField(max_length=200)
    descricao = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    dificuldade = models.CharField(max_length=20, choices=DIFICULDADE, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='destinos')
    criador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='destinos_criados')
    aprovado = models.BooleanField(default=False)
    distancia_km = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text='Extensão da trilha em km')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Destino'
        verbose_name_plural = 'Destinos'
        ordering = ['-created_at']

    def __str__(self):
        return self.nome

    @property
    def media_avaliacao(self):
        avals = self.avaliacoes.all()
        if not avals:
            return 0
        return round(sum(a.nota for a in avals) / len(avals), 1)

    @property
    def total_avaliacoes(self):
        return self.avaliacoes.count()

    @property
    def foto_principal(self):
        foto = self.fotos.first()
        return foto.url if foto else None


class FotoDestino(models.Model):
    destino = models.ForeignKey(Destino, on_delete=models.CASCADE, related_name='fotos')
    url = models.TextField()
    legenda = models.CharField(max_length=255, blank=True)
    ordem = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f'Foto de {self.destino.nome}'


class Avaliacao(models.Model):
    destino = models.ForeignKey(Destino, on_delete=models.CASCADE, related_name='avaliacoes')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('destino', 'usuario')
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'

    def __str__(self):
        return f'{self.usuario} avaliou {self.destino} com {self.nota} estrelas'


class Favorito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favoritos')
    destino = models.ForeignKey(Destino, on_delete=models.CASCADE, related_name='favoritado_por')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'destino')

    def __str__(self):
        return f'{self.usuario} favoritou {self.destino}'
