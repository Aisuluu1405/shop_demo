from django.views.generic import ListView, DetailView, CreateView

from webapp.models import Order, OrderProduct, Product


class OrderListView(ListView):
    template_name = 'order/list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        if self.request.user.has_perm('webapp:view_order'):
            return Order.objects.all().order_by('-created_at')
        return self.request.user.orders.all().order_by('-created_at')


class OrderDetailView(DetailView):
    template_name = 'order/detail.html'
    context_object_name = 'order'


    def get_queryset(self):
        if self.request.user.has_perm('webapp:view_order'):
            return Order.objects.all().order_by('-created_at')
        return self.request.user.orders.all()


class OrderCreateView(CreateView):
    model = Order

