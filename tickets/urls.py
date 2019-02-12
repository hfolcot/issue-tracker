from django.contrib import admin
from django.urls import path
from .views import bug_ticket_view, new_bug_view, new_feature_view, feature_ticket_view

urlpatterns = [
	path('bugs/<int:id>', bug_ticket_view, name="bug"),
	path('bugs/new', new_bug_view, name="new_bug"),
	path('features/<int:id>', feature_ticket_view, name="feature"),
	path('features/new', new_feature_view, name="new_feature"),
]