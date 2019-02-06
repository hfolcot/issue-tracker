from django.contrib import admin
from .models import Profile, DeveloperProfile

# Register your models here.

admin.site.register(Profile)
admin.site.register(DeveloperProfile)