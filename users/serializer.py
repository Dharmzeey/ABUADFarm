from itertools import product
from rest_framework import serializers

from .models import Goods
from products.models import Product

class ProductSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = ["name"]
    
class GoodsSerializer(serializers.ModelSerializer):
  # item = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
  item = ProductSerializer()
  class Meta:
    model = Goods
    fields = ['item', 'quantity', 'price', 'date_ordered']
    