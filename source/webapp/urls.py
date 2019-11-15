from django.urls import path
from webapp.views.basket_views import BasketView, BasketChangeView
from webapp.views.product_views import IndexView, ProductCreateView, ProductView, ProductEditView

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/<int:pk>/', ProductView.as_view(), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', ProductEditView.as_view(), name='product_edit'),
    path('basket/change/', BasketChangeView.as_view(), name='basket_change'),
    path('basket/', BasketView.as_view(), name='basket')
]
