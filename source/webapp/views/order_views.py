from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.base import View

from webapp.forms import ManualOrderForm, OrderProductForm
from webapp.mixins import StatsMixin
from webapp.models import Order, OrderProduct, Product, ORDER_STATUS_DELIVERED, ORDER_STATUS_CANCELED


class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'order/list.html'
    model = Order
    context_object_name = 'orders'

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


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order/detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        if self.request.user.has_perm('webapp:view_order'):
            return Order.objects.all().order_by('-created_at')
        return self.request.user.orders.all()


class OrderUpdateView(PermissionRequiredMixin, UpdateView):
    model = Order
    pass
    form_class = ManualOrderForm
    template_name = 'order/update.html'
    context_object_name = 'order'
    permission_required = 'webapp.change_order'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.pk})


class OrderDeliverView(PermissionRequiredMixin, View):
    permission_required = 'webapp.deliver_order'

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs.get('pk'))
        order.status = ORDER_STATUS_DELIVERED
        order.save()
        return redirect('webapp:order')


class OrderCancelView(PermissionRequiredMixin, View):
    permission_required = 'webapp.delete_order'

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs.get('pk'))
        order.status = ORDER_STATUS_CANCELED
        order.save()
        return redirect('webapp:order')


class OrderProductCreateView(PermissionRequiredMixin, CreateView):
    model = OrderProduct
    form_class = OrderProductForm
    template_name = 'order_product/create.html'
    permission_required = 'webapp.create_orderproduct'

    def get_context_data(self, **kwargs):
        kwargs['order'] = self.get_order()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.order = self.get_order()
        return super().form_valid(form)

    def get_order(self):
        return get_object_or_404(Order, pk=self.kwargs.get('pk'))

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})