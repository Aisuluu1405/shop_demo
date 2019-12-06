from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, DjangoModelPermissions, SAFE_METHODS
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from webapp.models import Product, Order, OrderProduct
from api_v2.serializers import ProductSerializer, OrderSerializer, OrderProductSerializer


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user.auth_token.delete()
        return Response({'status': 'ok'})


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class =  ProductSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        else:
            return super().get_permissions()

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderProductViewSet(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer

