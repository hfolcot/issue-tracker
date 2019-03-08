from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('bugtickets', views.BugTicketApiView)
router.register('featuretickets', views.FeatureTicketApiView)
router.register('ticketupdates', views.TicketUpdateApiView)

urlpatterns = [
	path('bugs/<int:id>', views.bug_ticket_view, name="bug"),
	path('bugs/new', views.new_bug_view, name="new_bug"),
	path('features/<int:id>', views.feature_ticket_view, name="feature"),
	path('features/new', views.new_feature_view, name="new_feature"),
	path('api/', include(router.urls)),
	path('api/auth', include('rest_framework.urls')),
]