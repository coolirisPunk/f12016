from .views import *
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.conf.urls import patterns, url, include
from rest_framework_nested import routers
from allauth.account.views import confirm_email
from django.views.generic import TemplateView, RedirectView
from allauth.account.views import confirm_email as allauthemailconfirmation

router = DefaultRouter()
router.register(r'user', UserProfileViewSet, base_name='user')
urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    #url(r'^rest-auth/user-profile/', UserProfileViewSet.as_view({'get': 'list', 'post':'create'}), name='user_profile'),
	url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^rest-auth/twitter/$', TwitterLogin.as_view(), name='twitter_login'),
    # this url is used to generate email content
    url(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'),
        url(r'^account-confirm-email/(?P<key>\w+)/$', TemplateView.as_view(template_name="email_verification.html"),
        name='account_confirm_email'),
	url(r'^rest-auth/user-profile/', include(router.urls)),
]
