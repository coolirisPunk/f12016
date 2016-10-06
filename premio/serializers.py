from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from common.serializers import DynamicFieldsModelSerializer
from rest_framework import serializers
from django.conf import settings
from django.contrib.sites.models import Site

domain_url = Site.objects.get_current().domain

class EventSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'description', 'start_time', 'ordering','slug','date','highlight'
        ]
        depth = 1
        order_by = (('ordering',))

class BenefitSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Benefit
        fields = [
            'id', 'button_text', 'link_url', 'description'
        ]

class EventTypeSerializer(DynamicFieldsModelSerializer):
    events = EventSerializer(many=True, read_only=True)
    class Meta:
        model = EventType
        fields = [
            'id', 'description', 'ordering', "events"
        ]
        depth = 1

class EventDaySerializer(DynamicFieldsModelSerializer):
    event_types = EventTypeSerializer(many=True, read_only=True)
    class Meta:
        model = EventDay
        fields = [
            'id','description','date','event_types'
        ]


class CategoryNewSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = CategoryNew
        fields = [
            'id','description',"ordering"
        ]


class NewListSerializer(DynamicFieldsModelSerializer):
    width_thumbnail  = serializers.SerializerMethodField('get_thumbnail_width')
    height_thumbnail  = serializers.SerializerMethodField('get_thumbnail_height')
    width_picture = serializers.SerializerMethodField('get_picture_width')
    height_picture = serializers.SerializerMethodField('get_picture_height')
    class Meta:
        model = New
        fields = [
            'id',"title","description","date","thumbnail","picture","post_url","category_new",
            "width_thumbnail","height_thumbnail","width_picture", "height_picture"
        ]

    def get_picture_width(self, obj):
        return '%s' % (obj.picture.width)

    def get_picture_height(self, obj):
        return '%s' % (obj.picture.height)

    def get_thumbnail_width(self, obj):
        return '%s' % (obj.thumbnail.width)

    def get_thumbnail_height(self, obj):
        return '%s' % (obj.thumbnail.height)

class NewItemSerializer(DynamicFieldsModelSerializer):
    thumbnail = serializers.SerializerMethodField('get_thumbnail_url')
    picture = serializers.SerializerMethodField('get_picture_url')

    width_thumbnail  = serializers.SerializerMethodField('get_thumbnail_width')
    height_thumbnail  = serializers.SerializerMethodField('get_thumbnail_height')
    width_picture = serializers.SerializerMethodField('get_picture_width')
    height_picture = serializers.SerializerMethodField('get_picture_height')

    class Meta:
        model = New
        fields = [
            'id',"title","description","date","thumbnail","picture","post_url","category_new",
            "width_thumbnail","height_thumbnail","width_picture", "height_picture"
        ]
    def get_thumbnail_url(self, obj):
        return '%s%s%s' % (domain_url, settings.MEDIA_URL, obj.thumbnail)

    def get_picture_url(self, obj):
        return '%s%s%s' % (domain_url, settings.MEDIA_URL, obj.picture)


    def get_picture_width(self, obj):
        return '%s' % (obj.picture.width)

    def get_picture_height(self, obj):
        return '%s' % (obj.picture.height)

    def get_thumbnail_width(self, obj):
        return '%s' % (obj.thumbnail.width)

    def get_thumbnail_height(self, obj):
        return '%s' % (obj.thumbnail.height)


class PremioListSerializer(DynamicFieldsModelSerializer):
    picture = serializers.SerializerMethodField('get_picture_url')
    flag = serializers.SerializerMethodField('get_flag_url')
    class Meta:
        model = Race
        fields = [
            'id','name','picture','flag'
        ]

    def get_picture_url(self, obj):
        return '%s%s%s' % (domain_url, settings.MEDIA_URL, obj.picture)


    def get_flag_url(self, obj):
        return '%s%s%s' % (domain_url, settings.MEDIA_URL, obj.flag)



class PremioDetailSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Race
        fields = [
            'id','name'
        ]

class PilotoListSerializer(DynamicFieldsModelSerializer):
    picture = serializers.SerializerMethodField('get_picture_url')
    
    class Meta:
        model = Driver
        fields = [
            'id','name','picture'
        ]

    def get_picture_url(self, obj):
        return '%s%s%s' % (domain_url, settings.MEDIA_URL, obj.picture)



class PilotoDetailSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Driver
        fields = [
            'id','name'
        ]


class HotelSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Hotel
        fields = [
            'id', 'name', 'location', 'website', 'phone','picture','latitude','longitude','ordering'
        ]


class RestauranteSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'location', 'phone', 'picture', 'latitude','longitude','ordering'
        ]

class LugarVisitarSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Place
        fields = [
            'id', 'name', 'location', 'exposition', 'phone','picture','latitude','longitude','ordering'
        ]


class Formula1TasteSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Formula1Taste
        fields = [
            'id', 'name', 'chef', 'website', 'picture','location','ordering'
        ]

class ZoneSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Zone
        fields = [
            'id', 'title'
        ]

class GrandstandSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Grandstand
        fields = [
            'id', 'title'
        ]



class SectionSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Section
        fields = [
            'id', 'title','latitude','longitude'
        ]


class RowSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Row
        fields = [
            'id', 'title'
        ]


class SeatSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Seat
        fields = [
            'id', 'title'
        ]