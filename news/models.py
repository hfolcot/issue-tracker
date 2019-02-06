from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from comments.models import get_sentinel_user

# Create your models here.

class Article(models.Model):
	"""
	News article for the blog
	"""
	title = models.CharField(max_length=250)
	content = models.TextField()
	author = models.ForeignKey(settings.AUTH_USER_MODEL, 
					default=1,
        			on_delete=models.SET(get_sentinel_user))
	timestamp = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return f"{self.id}"

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type