from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    foto_perfil = models.TextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    seguidores = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='seguindo',
        blank=True,
    )

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def total_seguidores(self):
        return self.seguidores.count()

    @property
    def total_seguindo(self):
        return self.seguindo.count()
