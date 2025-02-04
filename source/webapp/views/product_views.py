from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.models import Product
from webapp.mixins import StatsMixin


class IndexView(StatsMixin, ListView):
    model = Product
    template_name = 'index.html'


class ProductView(StatsMixin, DetailView):
    model = Product
    template_name = 'product/detail.html'


class ProductCreateView(PermissionRequiredMixin, StatsMixin, CreateView):
    model = Product
    template_name = 'product/create.html'
    fields = ('name', 'category', 'price', 'photo')
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.add_product'
    permission_denied_message = "Доступ запрещен"


class ProductEditView(PermissionRequiredMixin, StatsMixin, UpdateView):
    template_name = 'product/edit.html'
    model = Product
    fields = ('name', 'category', 'price', 'photo')
    context_object_name = 'product'
    permission_required = 'webapp.change_product'
    permission_denied_message = 'Доступ запрещен!'

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(PermissionRequiredMixin, StatsMixin, DeleteView):
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('webapp:index')
    context_object_name = 'product'
    permission_required = 'webapp.delete_product'
    permission_denied_message = 'Доступ запрещен!'

    def delete(self, request, *args, **kwargs):
        product = self.object = self.get_object()
        product.in_order = False
        product.save()
        return HttpResponseRedirect(self.get_success_url())


