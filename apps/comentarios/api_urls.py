from django.urls import path
from . import api_views

urlpatterns = [
    path('destino/<int:destino_id>/', api_views.ComentarioListCreateView.as_view(), name='api-comentarios'),
    path('<int:pk>/', api_views.ComentarioDeleteView.as_view(), name='api-comentario-delete'),
]
