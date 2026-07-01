from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Destino, Categoria, Favorito
from .utils import haversine


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categorias'] = Categoria.objects.all()
        return ctx


class DestinoListView(TemplateView):
    template_name = 'destinos/list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categorias'] = Categoria.objects.all()
        ctx['categoria_sel'] = self.request.GET.get('categoria', '')
        ctx['dificuldade_sel'] = self.request.GET.get('dificuldade', '')
        ctx['search'] = self.request.GET.get('search', '')
        ctx['lat'] = self.request.GET.get('lat', '')
        ctx['lon'] = self.request.GET.get('lon', '')
        ctx['raio'] = self.request.GET.get('raio', '50')
        return ctx


class DestinoDetailView(DetailView):
    model = Destino
    template_name = 'destinos/detail.html'
    context_object_name = 'destino'

    def get_queryset(self):
        return Destino.objects.filter(aprovado=True).select_related('categoria', 'criador').prefetch_related(
            'fotos', 'avaliacoes__usuario', 'comentarios__usuario',
            'grupos__criador', 'grupos__membros', 'pontos_encontro__criador'
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        destino = self.object
        ctx['grupos'] = destino.grupos.all()
        ctx['pontos_encontro'] = destino.pontos_encontro.all()
        ctx['comentarios'] = destino.comentarios.filter(parent__isnull=True).select_related('usuario').prefetch_related('respostas__usuario')
        if self.request.user.is_authenticated:
            ctx['favoritado'] = Favorito.objects.filter(usuario=self.request.user, destino=destino).exists()
            try:
                ctx['minha_nota'] = destino.avaliacoes.get(usuario=self.request.user).nota
            except Exception:
                ctx['minha_nota'] = 0
        return ctx


class DestinoCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'destinos/create.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categorias'] = Categoria.objects.all()
        return ctx
