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



# class UserProfileViewSet(RetrieveUpdateAPIView):
#     """
#     Returns User's details in JSON format.
#     Accepts the following GET parameters: token
#     Accepts the following POST parameters:
#         Required: token
#         Optional: email, first_name, last_name and UserProfile fields
#     Returns the updated UserProfile and/or User object.
#     """

#     serializer_class = UserProfileSerializer
#     permission_classes = (IsAuthenticated,)


#     def get_object(self):
#         #print self.request.user.pk
#         #print self.request.user.email
#         #print self.request.user.username
#         return self.request.user.user_profile


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

    def create(self,request, *args, **kwargs):
        user = self.request.user
        if user is not None:
            request.data["user"] = user.pk
            request.data["username"] = user.username
            request.data["first_name"] = user.first_name
            request.data["last_name"] = user.last_name
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, client_pk=None):
        queryset = UserProfile.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"results": serializer.data})

    def retrieve(self, request, pk=None):

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
