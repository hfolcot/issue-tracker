from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models



# Create your models here.

class Vote(models.Model):
	positive_vote = models.BooleanField()
	user = models.ForeignKey(User, null=True,
        			on_delete=models.CASCADE,)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	def __str__(self):
		return '{0} - {1} - {2}'.format(self.positive_vote, self.content_type, self.object_id)
