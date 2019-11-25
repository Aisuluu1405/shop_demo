from django.urls import path
from webapp.views.basket_views import BasketView, BasketChangeView
from webapp.views.product_views import IndexView, ProductCreateView, ProductView, ProductEditView, ProductDeleteView
from webapp.views.order_views import OrderListView, OrderCreateView, OrderDetailView, OrderDeleteView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', ProductView.as_view(), name='product_detail'),
    path('products/<int:pk>/edit/', ProductEditView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('basket/change/', BasketChangeView.as_view(), name='basket_change'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('order/', OrderListView.as_view(), name='order'),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order/<int:pk>/delete', OrderDeleteView.as_view(), name='order_delete'),
]
