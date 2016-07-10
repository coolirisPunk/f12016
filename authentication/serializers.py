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
            'id','zone','grada','section','fila','seat'
            ]

class UserCustomSerializer(DynamicFieldsModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)
    class Meta:
        model = UserModel
        fields = [
            'id','username','email','first_name','last_name','user_profile'
        ]


