from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from common.serializers import DynamicFieldsModelSerializer
from .models import *
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserCustomSerializer(DynamicFieldsModelSerializer):
    profile_id = serializers.CharField(source='user_profile.pk', read_only=True)
    zone = serializers.CharField(source='user_profile.zone', read_only=True)
    grada = serializers.CharField(source='user_profile.grada', read_only=True)
    section = serializers.CharField(source='user_profile.section', read_only=True)
    fila = serializers.CharField(source='user_profile.fila', read_only=True)
    seat = serializers.CharField(source='user_profile.seat', read_only=True)
    speed_lover = serializers.CharField(source='user_profile.speed_lover', read_only=True)

    class Meta:
        model = UserModel
        fields = [
            'id', 'username','email','first_name','last_name','profile_id','zone','grada','section','fila','seat','speed_lover'
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
            'id', 'zone', 'grada', 'section', 'fila', 'seat','speed_lover'
        ]

    def create(self, validated_data):
        print validated_data
        profile_data = validated_data.pop('user', None)
        request = self.context.get("request", None)
        if request and hasattr(request, "user"):
            user = request.user
            validated_data['user_id'] = user.pk

        return UserProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
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