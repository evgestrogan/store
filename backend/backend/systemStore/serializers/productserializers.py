from rest_framework import serializers
from .category_serializers import CategorySerializer


class PhotoProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    photo = serializers.CharField(max_length=150)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=150)
    photo = PhotoProductSerializer(many=True, read_only=True)
    description = serializers.CharField()
    weight = serializers.DecimalField(max_digits=5, decimal_places=3)
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    presence = serializers.BooleanField()
    category = CategorySerializer()



