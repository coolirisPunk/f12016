from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib.auth.hashers import make_password,is_password_usable,PBKDF2PasswordHasher, check_password


# Register your models here.


class UserResource(resources.ModelResource):

    class Meta:
        model = User

    def before_save_instance(self, instance, using_transactions, dry_run):
    	print instance.password
    	password = make_password(instance.password)
    	if is_password_usable(password):
    		print "usable"
    	else:
    		print "not usable"

    	if check_password(instance.password, password):
    		print "coinciden"
    	else:
    		print "no coincide"

    	instance.set_password(password)
        instance.password = password
    	print "Before"
    	pass


class UserProfileInline(admin.TabularInline):
    model = UserProfile

class UserAdmin(BaseUserAdmin, ImportExportModelAdmin):
	model = User
	inlines = [UserProfileInline]
	list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
	list_filter = ('is_staff', 'is_superuser')
	resource_class = UserResource






admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
	model = UserProfile
	#inlines = [UserProfileInline,]


admin.site.register(UserProfile, UserProfileAdmin)
