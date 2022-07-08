from .models import *
from rest_framework import serializers

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = ['author','review_id','rating','comment','reply']
    def get_author(self,instance):
        return str(instance.written_by.username)

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True)
    class Meta:
        model = Product
        fields = ['product_id','image','body','reviews']

class EditProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['image','body']