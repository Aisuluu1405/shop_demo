from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.base import View
from webapp.mixins import StatsMixin
from webapp.forms import ManualOrderForm, OrderProductForm, ProductsFormset
from webapp.models import Order, OrderProduct, ORDER_STATUS_DELIVERED, ORDER_STATUS_CANCELED, Product


class OrderListView(LoginRequiredMixin, StatsMixin, ListView):
    template_name = 'order/list.html'
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        if self.request.user.has_perm('webapp.view_order'):
            return Order.objects.all().order_by('-created_at')
        return self.request.user.orders.all().order_by('-created_at')


class OrderCreateView(PermissionRequiredMixin, StatsMixin, CreateView):
    model = Order
    form_class = ManualOrderForm
    template_name = 'order/create.html'
    permission_required = 'webapp.add_order'

    def get_context_data(self, **kwargs):
        if 'formset' not in kwargs:
            kwargs['formset'] = ProductsFormset()
        kwargs['product_list'] = Product.objects.filter(in_order=True)
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = ProductsFormset(data=request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.pk})


class OrderDetailView(LoginRequiredMixin, StatsMixin, DetailView):
    model = Order
    template_name = 'order/detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        if self.request.user.has_perm('webapp:view_order'):
            return Order.objects.all().order_by('-created_at')
        return self.request.user.orders.all()


class OrderUpdateView(PermissionRequiredMixin, StatsMixin, UpdateView):
    model = Order
    pass
    form_class = ManualOrderForm
    template_name = 'order/update.html'
    context_object_name = 'order'
    permission_required = 'webapp.change_order'

    def get_context_data(self, **kwargs):
        if 'formset' not in kwargs:
            kwargs['formset'] = ProductsFormset(instance=self.object)
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = ProductsFormset(instance=self.object, data=request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

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


class OrderProductCreateView(PermissionRequiredMixin, StatsMixin, CreateView):
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


class OrderProductUpdateView(PermissionRequiredMixin, StatsMixin, UpdateView):
    model = OrderProduct
    form_class = OrderProductForm
    context_object_name = 'order_product'
    template_name = 'order_product/update.html'
    permission_required = 'webapp.change_orderproduct'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})


class OrderProductDeleteView(PermissionRequiredMixin, StatsMixin, DeleteView):
    model = OrderProduct
    pass
    template_name = 'order_product/delete.html'
    context_object_name = 'order_product'
    permission_required = 'webapp.delete_orderproduct'

    def get_success_url(self):
        return reverse('webapp:order_detail', kwargs={'pk': self.object.order.pk})