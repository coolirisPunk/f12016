from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from common.serializers import DynamicFieldsModelSerializer
from .models import *
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserProfileSerializer(DynamicFieldsModelSerializer):
    #car = CarSerializer(read_only=True)
    #hotels = HotelSerializer(many=True, read_only=True)
    class Meta:
        model = UserProfile
        fields = [
            'id','zone','grada','section','fila','seat','user'
            ]

class UserCustomSerializer(DynamicFieldsModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = UserModel
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'user_profile'
        ]



class UserProfileCustomSerializer(DynamicFieldsModelSerializer):
    #user_profile = UserProfileSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    userid = serializers.CharField(source='user.pk', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = UserProfile
        fields = [
            'userid', 'username', 'email', 'first_name', 'last_name',
            'id', 'zone', 'grada', 'section', 'fila', 'seat'
        ]


    def update(self, instance, validated_data):
        print instance
        print validated_data
        profile_data = validated_data.pop('user', None)
        if profile_data is not None:
            current_profile = instance.user
            for attr, value in profile_data.items():
                setattr(current_profile, attr, value)
            current_profile.save()

        instance.zone = validated_data.get('zone', instance.zone)
        instance.grada = validated_data.get('grada', instance.grada)
        instance.section = validated_data.get('section', instance.section)
        instance.fila = validated_data.get('fila', instance.fila)
        instance.seat = validated_data.get('seat', instance.seat)
        instance.speed_lover = validated_data.get('speed_lover', instance.speed_lover)
        instance.save()
        return instance