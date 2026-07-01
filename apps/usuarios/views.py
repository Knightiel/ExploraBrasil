from django.views.generic import TemplateView, DetailView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from .models import Usuario
from apps.destinos.models import Favorito


class LoginView(TemplateView):
    template_name = 'usuarios/login.html'

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', '/'))
        return self.render_to_response(self.get_context_data(error='Usuário ou senha inválidos.'))


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect('/')


class RegisterView(TemplateView):
    template_name = 'usuarios/register.html'

    def post(self, request):
        from apps.usuarios.serializers import RegisterSerializer
        data = {
            'username': request.POST.get('username'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'password2': request.POST.get('password2'),
            'bio': request.POST.get('bio', ''),
        }
        s = RegisterSerializer(data=data)
        if s.is_valid():
            user = s.save()
            login(request, user)
            return redirect('/')
        return self.render_to_response(self.get_context_data(errors=s.errors))


class PerfilView(TemplateView):
    template_name = 'usuarios/profile.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = get_object_or_404(Usuario, pk=kwargs['pk'])
        ctx['perfil'] = user
        ctx['destinos'] = user.destinos_criados.filter(aprovado=True)[:6]
        ctx['grupos'] = user.grupos_participando.all()[:4]
        if self.request.user.is_authenticated:
            ctx['seguindo'] = self.request.user.seguindo.filter(pk=user.pk).exists()
        return ctx


class FavoritosView(LoginRequiredMixin, TemplateView):
    template_name = 'usuarios/favorites.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['favoritos'] = Favorito.objects.filter(
            usuario=self.request.user
        ).select_related('destino__categoria').prefetch_related('destino__fotos', 'destino__avaliacoes')
        return ctx
