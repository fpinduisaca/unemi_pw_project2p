# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from .forms import ClienteForm
from .models import Cliente


class ClientesListView(LoginRequiredMixin, ListView):
    context_object_name = 'clientes'
    model = Cliente
    # template_name = 'clientes/cliente_list.html'
    # group_required = ['trabajadores']


# Create your views here.
class ClientesDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    # template_name = 'clientes/cliente_detail.html'


class ClientesUpdateView(UpdateView):
    form_class = ClienteForm
    # template_name = 'clientes/cliente_form.html'
    model = Cliente
    success_url = '/clientes'


class ClientesDeleteView(DeleteView):
    model = Cliente
    success_url = '/clientes'
    # template_name = 'clientes/cliente_confirm_delete.html'
    # group_required = ['administrador']


class ClientesCreateView(LoginRequiredMixin, CreateView):
    form_class = ClienteForm
    # template_name = 'clientes/cliente_form.html'
    model = Cliente
    success_url = '/clientes'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
