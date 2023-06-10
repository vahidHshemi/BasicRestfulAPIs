from rest_framework import serializers
from decimal import Decimal

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=800)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    
    # creating customize serializer fields
    price_with_tax = serializers.SerializerMethodField(method_name='claculate_tax')
    
    def claculate_tax(self, unit_price):
        return unit_price * Decimal(1.1)

class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)