from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from common.serializers import DynamicFieldsModelSerializer


class CategoryProductSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = CategoryProduct
        fields = [
            'id', 'name', 'picture',
        ]


class SellerSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Seller
        fields = [
            'id', 'name', 'picture',
        ]


class ProductSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'name', "picture" ,'description', 'price','review',
        ]
