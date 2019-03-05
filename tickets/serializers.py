from rest_framework import serializers
from .models import BugTicket, NewFeatureTicket, TicketUpdate

class BugSerializer(serializers.ModelSerializer):
	"""
	Convert bug tickets into JSON for the API
	"""
	class Meta:
		model = BugTicket
		fields = (
			'id', 
			'customer', 
			'title', 
			'description', 
			'timestamp', 
			'assigned', 
			'status', 
			'priority', 
			'votes', 
			'time_spent', 
			'last_update',
			'rating',
			'fixed_date')

class FeatureSerializer(serializers.ModelSerializer):
	"""
	Convert feature tickets into JSON for the API
	"""
	class Meta:
		model = NewFeatureTicket
		fields = (
			'id',
			'customer',
			'title',
			'description',
			'assigned',
			'quoted',	'cost',
			'status',
			'time_spent',
			'number_of_donations',
			'total_donations',
			'last_update',
			'votes',
			'rating',
			'implemented_date'
			)

class TicketUpdateSerializer(serializers.ModelSerializer):
	"""
	Convert ticket update info into JSON for the API
	"""
	class Meta:
		model = TicketUpdate
		fields = (
			'timestamp',
			'object_id',
			'content_type',
			'time_spent',
			'user'
		)
