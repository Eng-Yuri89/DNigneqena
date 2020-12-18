from django.contrib import admin
from users.models import UserProfile

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name','company','state', 'phone','country','image_tag']

admin.site.register(UserProfile,UserProfileAdmin)
