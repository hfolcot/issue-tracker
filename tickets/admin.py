from django.contrib import admin
from .models import BugTicket, NewFeatureTicket, Update

# Register your models here.
admin.site.register(BugTicket)
admin.site.register(NewFeatureTicket)
admin.site.register(Update)