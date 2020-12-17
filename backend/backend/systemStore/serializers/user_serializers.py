from rest_framework import serializers
from .productserializers import ProductSerializer
from systemAuthentication.models import User, DescriptionProductUser


class BasketCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    count = serializers.IntegerField()

    def create(self, validated_data):
        try:
            object = DescriptionProductUser.objects.get(user_id=validated_data['user_id'], product_id=validated_data['product_id'])
            object.count += validated_data['count']
            object.save()
            return object
        except:
            return DescriptionProductUser.objects.create(**validated_data)


class BasketSerializer(serializers.Serializer):
    product = ProductSerializer(many=True, read_only=True)
    user_to_product = BasketCreateSerializer(many=True, read_only=True)
