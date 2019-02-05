from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

def get_sentinel_user():
	#return 'deleted' on comments associated with deleted user accounts
    return get_user_model().objects.get_or_create(username='deleted')[0]



class Comment(models.Model):
	"""
	Model for comments on tickets and blog posts
	"""
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.SET(get_sentinel_user))
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	timestamp = models.DateTimeField(auto_now=True)
	content = models.TextField()

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return str(self.user.username)


	def get_comments(ticket_type, ticket_id):
		#Get comments for a specific ticket or post
		content_type = ContentType.objects.get_for_model(ticket_type)
		oid = ticket_id
		comments = Comment.objects.filter(content_type=content_type, object_id=oid)
		return comments