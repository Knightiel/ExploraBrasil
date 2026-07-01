from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.DestinoListCreateView.as_view(), name='api-destinos'),
    path('<int:pk>/', api_views.DestinoDetailView.as_view(), name='api-destino-detail'),
    path('<int:pk>/avaliar/', api_views.AvaliarView.as_view(), name='api-avaliar'),
    path('<int:pk>/favoritar/', api_views.FavoritarView.as_view(), name='api-favoritar'),
    path('categorias/', api_views.CategoriaListView.as_view(), name='api-categorias'),
]
