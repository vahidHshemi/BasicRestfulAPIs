from gc import collect
from rest_framework import serializers
from decimal import Decimal
from .models import Collection

class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=800)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    
    # creating customize serializer fields
    price_with_tax = serializers.SerializerMethodField(method_name='claculate_tax')
    
    def claculate_tax(self, Product):
        return Product.unit_price * Decimal(1.1)
    
    # Serializing Relationships
    # based on primary_key
    # collection = serializers.PrimaryKeyRelatedField(read_only=True)
    # based on StringRelatedField
    # collection = serializers.StringRelatedField(read_only=True)
    # based on nested objects
    # collection = CollectionSerializer()
    # based on hyperlinkfield()
    collection = serializers.HyperlinkedRelatedField(queryset=Collection.objects.all(), view_name='collection_detail')

