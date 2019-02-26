from django.contrib import admin
from .models import BugTicket, NewFeatureTicket

# Register your models here.
admin.site.register(BugTicket)
admin.site.register(NewFeatureTicket)