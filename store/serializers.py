from dataclasses import field, fields
from rest_framework import serializers
from decimal import Decimal
from .models import Collection, Product

# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=100)

# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=100)
#     description = serializers.CharField(max_length=800)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    
    # creating customize serializer fields
    # price_with_tax = serializers.SerializerMethodField(method_name='claculate_tax')
    
    # def claculate_tax(self, Product):
    #     return Product.unit_price * Decimal(1.1)
    
    # Serializing Relationships
    # based on primary_key
    # collection = serializers.PrimaryKeyRelatedField(read_only=True)
    # based on StringRelatedField
    # collection = serializers.StringRelatedField(read_only=True)
    # based on nested objects
    # collection = CollectionSerializer()
    # based on hyperlinkfield()
    # collection = serializers.HyperlinkedRelatedField(queryset=Collection.objects.all(), view_name='collection_detail')

# Model Serializer
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
    
    products_count = serializers.IntegerField()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']
    
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_price')
    
    def calculate_price(self, Product: Product):
        return Product.unit_price * Decimal(1.1)
    
    # collection = serializers.HyperlinkedRelatedField(queryset=Collection.objects.all(), view_name='collection_detail')
    
    # when you need to set special fields or ...
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product
    
    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance
    
    

