from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


from accounts.models import Profile

# Create your models here.

class Vote(models.Model):
	positive_vote = models.BooleanField()
	user = models.ForeignKey(Profile, null=True,
        			on_delete=models.CASCADE,)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	def get_votes(ticket_type, ticket_id):
		#Get votes for a specific ticket or post
		content_type = ContentType.objects.get_for_model(ticket_type)
		oid = ticket_id
		votes = Vote.objects.filter(content_type=content_type, object_id=oid)
		return votes
