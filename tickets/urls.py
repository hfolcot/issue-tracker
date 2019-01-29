from django.contrib import admin
from django.urls import path
from .views import all_tickets, bug_ticket

urlpatterns = [
	path('', all_tickets, name="all_tickets"),
	path('bugs/<int:id>', bug_ticket, name="bugs")
]