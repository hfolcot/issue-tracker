from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from .views import all_tickets

urlpatterns = [
	path('/', all_tickets, name="all_tickets")
]