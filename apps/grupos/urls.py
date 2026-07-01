from django.urls import path
from . import views

urlpatterns = [
    path('', views.GrupoListView.as_view(), name='grupos-list'),
    path('<int:pk>/', views.GrupoDetailView.as_view(), name='grupo-detail'),
]
