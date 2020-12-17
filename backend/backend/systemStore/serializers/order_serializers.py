from rest_framework import serializers
from ..models import DescriptionProductOrder, Order
from .productserializers import ProductSerializer


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    product = ProductSerializer(read_only=True, many=True)
    status = serializers.CharField(read_only=True)
    created = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Order.objects.create(**validated_data)


class DescriptionProductOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    count = serializers.IntegerField()

    def create(self, validated_data):
        return DescriptionProductOrder.objects.create(**validated_data)
