from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import viewsets, mixins
from common.mixins import CustomFieldsMixin, ActiveDesactiveMixin
from request_log.mixins import LoggingMixin
from rest_framework import viewsets, mixins
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from django.shortcuts import get_list_or_404, get_object_or_404
from django.conf import settings

class CategoryProductViewSet(viewsets.ViewSet):
    serializer_class = CategoryProductSerializer

    def list(self, request,):
        queryset = CategoryProduct.objects.filter()
        serializer = CategoryProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = CategoryProduct.objects.filter()
        c_product = get_object_or_404(queryset, pk=pk)
        serializer = CategoryProductSerializer(c_product)
        return Response(serializer.data)

class SellerViewSet(viewsets.ViewSet):
    serializer_class = SellerSerializer

    def list(self, request, category_product_pk=None):
        queryset = Seller.objects.filter(category_product=category_product_pk)
        serializer = SellerSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, category_product_pk=None):
        queryset = Seller.objects.filter(pk=pk, category_product=category_product_pk)
        seller = get_object_or_404(queryset, pk=pk)
        serializer = SellerSerializer(seller)
        return Response(serializer.data)

class ProductViewSet(viewsets.ViewSet):
    serializer_class = ProductSerializer

    def list(self, request, category_product_pk=None, seller_pk=None):
        queryset = Product.objects.filter(seller__category_product=category_product_pk, seller=seller_pk)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, category_product_pk=None, seller_pk=None):
        queryset = Product.objects.filter(pk=pk, seller=seller_pk, seller__category_product=category_product_pk)
        product = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class ProductsWithoutCategoryViewSet(viewsets.ViewSet):
    serializer_class = ProductSerializer

    def list(self, request, category_product_pk=None):
        print category_product_pk
        queryset = Product.objects.filter(seller__category_product=category_product_pk)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, category_product_pk=None,):
        queryset = Product.objects.filter(pk=pk, seller__category_product=category_product_pk)
        product = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
