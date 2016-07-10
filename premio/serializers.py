from rest_framework.response import Response
from rest_framework import status
from .models import *
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from common.serializers import DynamicFieldsModelSerializer


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
            'id','short_title',"short_description","title","description","date","thumbnail","picture"
        ]

class NewItemSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = New
        fields = [
            'id','short_title',"short_description","title","description","date","thumbnail","picture"
        ]


class PremioListSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Race
        fields = [
            'id','name','picture'
        ]



class PremioDetailSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Race
        fields = [
            'id','name'
        ]

class PilotoListSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Race
        fields = [
            'id','name','picture'
        ]



class PilotoDetailSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Race
        fields = [
            'id','name'
        ]


class HotelSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Hotel
        fields = [
            'id', 'name', 'location', 'phone','picture','latitude','longitude','ordering'
        ]


class RestauranteSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'location', 'phone','picture','latitude','longitude','ordering'
        ]

class LugarVisitarSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Place
        fields = [
            'id', 'name', 'location', 'phone','picture','latitude','longitude','ordering'
        ]
