from django.http import Http404
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt import authentication

from .models import Category, Product, Order
from systemAuthentication.models import User, DescriptionProductUser
from .serializers.category_serializers import CategorySerializer
from .serializers.productserializers import ProductSerializer
from .serializers.user_serializers import BasketSerializer, BasketCreateSerializer
from .serializers.order_serializers import DescriptionProductOrderSerializer, OrderSerializer


class CategoryList(APIView):
    """
    Список категорй продуктов
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTTokenUserAuthentication, ]

    def get(self, request, format=None):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)


class ProductList(APIView):
    """
    Список категорй продуктов
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.JWTTokenUserAuthentication, ]

    def get(self, request, format=None):
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get(self, request, pk, format=None):
        product = Product.objects.all().filter(category=pk)
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data)


class BasketDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = BasketSerializer(snippet)
        return Response(serializer.data)


class BasketList(APIView):
    def post(self, request, format=None):
        serializer = BasketCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        print(request.data)
        object = DescriptionProductUser.objects.get(user_id=request.data['user_id'], product_id=request.data['product_id'])

        if object.count <= int(request.data['count']):
            object.delete()
        else:
            object.count -= int(request.data['count'])
            object.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DescriptionProductOrderList(APIView):
    def post(self, request, format=None):
        for product in request.data['products']:
            serializer = DescriptionProductOrderSerializer(data=product)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)


class OrderList(APIView):
    def get(self, request, format=None):
        snippets = Order.objects.all().filter(user_id=request.GET.get('user_id'))
        serializer = OrderSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)