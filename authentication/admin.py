from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.

class UserProfileInline(admin.TabularInline):
    model = UserProfile

class UserAdmin(admin.ModelAdmin):
	model = User
	inlines = [UserProfileInline,]



class UserProfileAdmin(admin.ModelAdmin):
	model = UserProfile
	#inlines = [UserProfileInline,]

#admin.site.unregister(User)
admin.site.register(UserProfile, UserProfileAdmin)




