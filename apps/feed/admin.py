from django.contrib import admin
from .models import Atividade

@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo', 'destino', 'grupo', 'created_at']
    list_filter = ['tipo']
