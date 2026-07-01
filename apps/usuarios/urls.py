from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('cadastro/', views.RegisterView.as_view(), name='register'),
    path('perfil/<int:pk>/', views.PerfilView.as_view(), name='perfil'),
    path('favoritos/', views.FavoritosView.as_view(), name='favoritos'),
]
