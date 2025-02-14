from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register the User model to the admin site
admin.site.register(User, UserAdmin)
