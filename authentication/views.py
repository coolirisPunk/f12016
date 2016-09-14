from django.shortcuts import render
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from rest_auth.views import LoginView
from rest_auth.social_serializers import TwitterLoginSerializer
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, mixins
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from common.mixins import CustomFieldsMixin, ActiveDesactiveMixin
from rest_framework.decorators import detail_route, list_route
from rest_framework import status



class FacebookLogin(LoggingMixin, SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class TwitterLogin(LoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


class ProfileViewSet(APIView):
    """
    List all snippets, or create a new snippet.
    Add a comment to this line
    """
    permission_classes = []

    def get(self, request):
    	if self.request.method == "GET":
    		print("get")

    	return Response("get")

    def post(self, request):
    	print("post")
        return Response("post")


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    User endpoints
    """
    serializer_class = UserProfileCustomSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]
    model = UserProfile


    def get_queryset(self):
        user = self.request.user
        queryset = UserProfile.objects.filter(user=user)
        return queryset

    def create(self, request, *args, **kwargs):
        user = self.request.user

        vip_party_racers = ["1 (Main Grandstand)", "2 (Main Grandstand)"]
        speed_lovers = ["2-A", "3", "4", "5", "6", "6-A"]
        true_racers = ["7", "8", "9", "10", "11"]
        euphoric_fans = ["14", "15"]

        if request.data["grada"] in vip_party_racers:
            request.data["speed_lover"] = "vip_party_racers"
        elif request.data["grada"] in speed_lovers:
            request.data["speed_lover"] = "speed_lovers"
        elif request.data["grada"] in true_racers:
            request.data["speed_lover"] = "true_racers"
        elif request.data["grada"] in euphoric_fans:
            request.data["speed_lover"] = "euphoric_fans"


        #if 'speed_lover' not in request.data:
        #    request.data["speed_lover"] = "speed_lovers"
        if user is not None:
            request.data["user"] = user.pk
            request.data["username"] = user.username
            request.data["first_name"] = "first_name"
            request.data["last_name"] = "last_name"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, client_pk=None):
        queryset = self.request.user
        serializer = UserCustomSerializer(queryset)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        user = self.request.user
        if user is not None:
            request.data["user"] = user.pk
            request.data["username"] = user.username
            request.data["first_name"] = "first_name"
            request.data["last_name"] = "last_name"
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
