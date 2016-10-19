from rest_framework.response import Response
from rest_framework import status, serializers
from .models import *
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from common.serializers import DynamicFieldsModelSerializer
from django.contrib.sites.models import Site
from django.conf import settings

domain_url = "http://" + Site.objects.get_current().domain


class CategoryProductSerializer(DynamicFieldsModelSerializer):
    picture = serializers.SerializerMethodField('get_picture_url')
    class Meta:
        model = CategoryProduct
        fields = [
            'id', 'name', 'picture',
        ]

    def get_picture_url(self, obj):
        return '%s%s%s' % (domain_url, settings.MEDIA_URL, obj.picture)


class SellerSerializer(DynamicFieldsModelSerializer):
    picture = serializers.SerializerMethodField('get_picture_url')
    class Meta:
        model = Seller
        fields = [
            'id', 'name', 'picture',
        ]

    def get_picture_url(self, obj):
        return '%s%s%s' % (domain_url, settings.MEDIA_URL, obj.picture)

class ProductSerializer(DynamicFieldsModelSerializer):
    #picture = serializers.SerializerMethodField('get_picture_url')
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'review',
        ]

    def get_picture_url(self, obj):
        return '%s%s%s' % (domain_url, settings.MEDIA_URL, obj.picture)
