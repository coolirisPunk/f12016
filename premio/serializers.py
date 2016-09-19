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
            'id', 'description', 'start_time', 'ordering'
        ]
        depth = 1
        order_by = (('ordering',))

class EventTypeSerializer(DynamicFieldsModelSerializer):
    events = EventSerializer(many=True, read_only=True)
    class Meta:
        model = EventType
        fields = [
            'id', 'description', 'ordering',"events"
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

    class Meta:
        model = New
        fields = [
            'id','short_title',"short_description","title","description","date","thumbnail","picture","post_url"
        ]

class NewItemSerializer(DynamicFieldsModelSerializer):
    thumbnail = serializers.SerializerMethodField('get_thumbnail_url')
    picture = serializers.SerializerMethodField('get_picture_url')
    class Meta:
        model = New
        fields = [
            'id','short_title',"short_description","title","description","date","thumbnail","picture","post_url"
        ]
    def get_thumbnail_url(self, obj):
        return '%s%s%s' % (domain_url, settings.MEDIA_URL, obj.thumbnail)

    def get_picture_url(self, obj):
        return '%s%s%s' % (domain_url, settings.MEDIA_URL, obj.picture)


class PremioListSerializer(DynamicFieldsModelSerializer):
    picture = serializers.SerializerMethodField('get_picture_url')

    class Meta:
        model = Race
        fields = [
            'id','name','picture','flag'
        ]

    def get_picture_url(self, obj):
        return '%s%s%s' % (domain_url, settings.MEDIA_URL, obj.picture)



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
            'id', 'name',  'chef','website', 'picture','latitude','longitude','ordering'
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
            'id', 'title'
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