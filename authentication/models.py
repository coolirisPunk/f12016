from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.utils.html import format_html
from django.conf.urls.static import static


class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name='user_profile')
    # custom fields for user
    zone = models.CharField(max_length=100,null=True, blank=True)
    grada = models.CharField(max_length=100,null=True, blank=True)
    section = models.CharField(max_length=10,null=True, blank=True)
    fila = models.CharField(max_length=10,null=True, blank=True)
    seat = models.CharField(max_length=10,null=True, blank=True)
    speed_lover_options = (
        ('speed_lovers', 'Speed Lovers',),
        ('euphoric_fans', 'Euphoric Fans',),
        ('true_racers', 'True Racers',),
        ('vip_party_racers', 'VIP Party Racers',),
    )
    speed_lover = models.CharField(choices=speed_lover_options, max_length=20)

    def __unicode__(self):
        return str(self.user.first_name)
