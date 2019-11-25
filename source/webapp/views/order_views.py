from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView

from webapp.forms import ManualOrderForm
from webapp.mixins import StatsMixin
from webapp.models import Order, OrderProduct, Product


class OrderListView(PermissionRequiredMixin, ListView):
    template_name = 'order/list.html'
    model = Order
    context_object_name = 'orders'
    permission_required = 'webapp.view_order'
    permission_denied_message = 'Доступ запрещен!'

    def get_queryset(self):
        if self.request.user.has_perm('webapp.view_order'):
            return Order.objects.all().order_by('-created_at')
        return self.request.user.orders.all().order_by('-created_at')


class OrderCreateView(PermissionRequiredMixin, CreateView):
    model = Order
    form_class = ManualOrderForm
    template_name = 'order/create.html'
    permission_required = 'webapp.add_order'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.pk})



class OrderDetailView(PermissionRequiredMixin, DetailView):
    template_name = 'order/detail.html'
    context_object_name = 'order'
    permission_required = 'webapp.view_order'
    permission_denied_message = 'Доступ запрещен!'


    def get_queryset(self):
        if self.request.user.has_perm('webapp:view_order'):
            return Order.objects.all().order_by('-created_at')
        return self.request.user.orders.all()


class OrderDeleteView(PermissionRequiredMixin, StatsMixin, DeleteView):
    model = Order
    template_name = 'order/delete.html'
    success_url = reverse_lazy('webapp:order_detail')
    context_object_name = 'product'
    permission_required = 'webapp.change_order'
    permission_denied_message = 'Доступ запрещен!'

    def delete(self, request, *args, **kwargs):
        order = self.object = self.get_object()
        order.status ='canceled'
        order.save()
        return HttpResponseRedirect(self.get_success_url())
