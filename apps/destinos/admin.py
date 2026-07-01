from django.contrib import admin
from .models import Categoria, Destino, FotoDestino, Avaliacao, Favorito


class FotoDestinoInline(admin.TabularInline):
    model = FotoDestino
    extra = 1


@admin.register(Destino)
class DestinoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'dificuldade', 'aprovado', 'criador', 'created_at']
    list_filter = ['aprovado', 'categoria', 'dificuldade']
    search_fields = ['nome', 'descricao']
    list_editable = ['aprovado']
    inlines = [FotoDestinoInline]
    actions = ['aprovar_destinos']

    def aprovar_destinos(self, request, queryset):
        queryset.update(aprovado=True)
        self.message_user(request, f'{queryset.count()} destino(s) aprovado(s).')
    aprovar_destinos.short_description = 'Aprovar destinos selecionados'


admin.site.register(Categoria)
admin.site.register(Avaliacao)
admin.site.register(Favorito)
