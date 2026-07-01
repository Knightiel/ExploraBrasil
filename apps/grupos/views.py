from django.views.generic import TemplateView
from .models import GrupoExpedicao


class GrupoListView(TemplateView):
    template_name = 'grupos/list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['grupos'] = GrupoExpedicao.objects.select_related('destino', 'criador').prefetch_related('membros').order_by('-created_at')
        return ctx


class GrupoDetailView(TemplateView):
    template_name = 'grupos/detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from django.shortcuts import get_object_or_404
        grupo = get_object_or_404(GrupoExpedicao, pk=kwargs['pk'])
        ctx['grupo'] = grupo
        ctx['pontos'] = grupo.pontos_encontro.all()
        if self.request.user.is_authenticated:
            ctx['membro'] = grupo.membros.filter(pk=self.request.user.pk).exists()
        return ctx
