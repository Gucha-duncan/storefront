from rest_framework import serializers
from decimal import Decimal

from .models import*

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title']

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','description', 'slug', 'inventory','unit_price', 'price_with_tax', 'collection' ]
      
    collection = CollectionSerializer(read_only=True)
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
    def calculate_tax(self, product: Product):
        return round(Decimal(product.unit_price) * Decimal('1.1'), 2)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['title', 'featured_product']
        