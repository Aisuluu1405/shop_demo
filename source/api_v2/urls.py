from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from .views import ProductViewSet, OrderViewSet, OrderProductViewSet, LogoutView

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'order-products', OrderProductViewSet)
router.register(r'orders', OrderViewSet)

app_name = 'api_v2'

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='obtain_auth_token'),
    path('logout/', LogoutView.as_view(), name='delete_auth_token')
]
