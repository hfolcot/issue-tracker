from django.urls import path
from .views import bug_ticket_view, new_bug_view, new_feature_view, feature_ticket_view, voting_view

urlpatterns = [
	path('bugs/<int:id>', bug_ticket_view, name="bug"),
	path('<str:content_type>/<int:object_id>/vote/<int:vote_type>', voting_view, name="bug_vote"),
	path('bugs/new', new_bug_view, name="new_bug"),
	path('features/<int:id>', feature_ticket_view, name="feature"),
	path('features/new', new_feature_view, name="new_feature"),
	path('features/<int:id>/vote/<str:score>', voting_view, name="feature_vote"),
]