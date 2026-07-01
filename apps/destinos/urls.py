from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('destinos/', views.DestinoListView.as_view(), name='destinos-list'),
    path('destinos/<int:pk>/', views.DestinoDetailView.as_view(), name='destino-detail'),
    path('destinos/novo/', views.DestinoCreateView.as_view(), name='destino-create'),
]
