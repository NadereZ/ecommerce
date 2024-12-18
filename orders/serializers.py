from rest_framework import serializers
from . models import Order

class OrderSelializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'product_name', 'quantity', 'price']