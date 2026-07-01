from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.GrupoListCreateView.as_view(), name='api-grupos'),
    path('<int:pk>/', api_views.GrupoDetailView.as_view(), name='api-grupo-detail'),
    path('<int:pk>/entrar/', api_views.EntrarGrupoView.as_view(), name='api-entrar-grupo'),
    path('<int:pk>/pontos-encontro/', api_views.PontoEncontroCreateView.as_view(), name='api-ponto-encontro'),
]
