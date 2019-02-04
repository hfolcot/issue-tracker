from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.



class BugTicket(models.Model):
	"""
	Model for a ticket describing a bug
	"""
	customer = models.ForeignKey(settings.AUTH_USER_MODEL, 
					default=1,
        			on_delete=models.CASCADE,)
	title = models.CharField(max_length=300, blank=False)
	description = models.TextField()
	timestamp = models.DateTimeField(auto_now=True)
	screenshot = models.ImageField(upload_to='images', blank=True)
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	fixed = models.BooleanField(default=False)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return f"tickets/bugs/{self.id}"

	class Meta:
		verbose_name = 'bugticket'

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type

class NewFeatureTicket(models.Model):
	title = models.CharField(max_length=300, blank=False)
	description = models.TextField()
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	quoted = models.BooleanField(default=False)
	cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
	implemented = models.BooleanField(default=False)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return f"tickets/features/{self.id}"