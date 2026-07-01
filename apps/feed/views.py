from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Atividade


class FeedView(LoginRequiredMixin, TemplateView):
    template_name = 'feed/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        seguindo_ids = self.request.user.seguindo.values_list('id', flat=True)
        ctx['atividades'] = Atividade.objects.filter(
            usuario_id__in=seguindo_ids
        ).select_related('usuario', 'destino', 'grupo', 'usuario_alvo')[:50]
        return ctx
