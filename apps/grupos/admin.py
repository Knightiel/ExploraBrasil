from django.contrib import admin
from .models import GrupoExpedicao, PontoEncontro

@admin.register(GrupoExpedicao)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'destino', 'criador', 'data_expedicao', 'vagas', 'total_membros']
    search_fields = ['nome']

admin.site.register(PontoEncontro)
