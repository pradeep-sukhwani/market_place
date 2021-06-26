from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import Product, Category, CustomUser


class CategorySerilizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'last_login', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff',
                  'is_active', 'date_joined']


class CustomUserSerializer(serializers.ModelSerializer):
    friends = UserSerializer(many=True)
    user = UserSerializer()
    

    class Meta:
        model = CustomUser
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerilizer(many=True, read_only=True)
    product_viewed = CustomUserSerializer(many=True, read_only=True)
    custom_id = serializers.IntegerField(read_only=True)
    is_available = serializers.BooleanField(default=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        last_custom_id = Product.objects.order_by('-added_on')[0].custom_id
        validated_data.update({'custom_id': last_custom_id + 1})
        instance = super(ProductSerializer, self).create(validated_data)
        return instance
