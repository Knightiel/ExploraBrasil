from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import api_views

urlpatterns = [
    path('register/', api_views.RegisterView.as_view(), name='api-register'),
    path('login/', api_views.LoginView.as_view(), name='api-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('me/', api_views.MeView.as_view(), name='api-me'),
    path('usuarios/<int:pk>/', api_views.UsuarioDetailView.as_view(), name='api-usuario-detail'),
    path('usuarios/<int:pk>/seguir/', api_views.SeguirView.as_view(), name='api-seguir'),
]
