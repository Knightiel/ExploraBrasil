from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
    fieldsets = UserAdmin.fieldsets + (
        ('Perfil', {'fields': ('foto_perfil', 'bio')}),
    )
