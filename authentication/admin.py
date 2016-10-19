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
	list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
	list_filter = ('is_staff', 'is_superuser')



admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
	model = UserProfile
	#inlines = [UserProfileInline,]

#admin.site.unregister(User)
admin.site.register(UserProfile, UserProfileAdmin)
