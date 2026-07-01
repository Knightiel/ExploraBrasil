from django.contrib import admin
from .models import Comentario

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'destino', 'texto', 'parent', 'created_at']
    list_filter = ['created_at']
    search_fields = ['texto', 'usuario__username']
