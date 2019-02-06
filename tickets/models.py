from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models

from accounts.models import DeveloperProfile

# Create your models here.



class BugTicket(models.Model):
	"""
	Model for a ticket describing a bug
	"""
	#Choices for priority and status
	CRITICAL = 'Critical'
	HIGH = 'High'
	MEDIUM = 'Medium'
	LOW = 'Low'
	PENDING = 'Pending'
	INPROGRESS = 'In Progress'
	FIXED = 'Fixed'

	PRIORITY_CHOICES = ((CRITICAL, 'Critical'), 
		(HIGH, 'High'), 
		(MEDIUM, 'Medium'), 
		(LOW, 'Low'))

	STATUS_CHOICES = ((PENDING,'Pending'),
		(INPROGRESS, 'In Progress'),
		(FIXED, 'Fixed'))



	customer = models.ForeignKey(settings.AUTH_USER_MODEL, 
					default=1,
        			on_delete=models.CASCADE,)
	title = models.CharField(max_length=300, blank=False)
	description = models.TextField()
	timestamp = models.DateTimeField(auto_now=True)
	screenshot = models.ImageField(upload_to='images', blank=True)
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	assigned = models.ForeignKey(DeveloperProfile, on_delete=models.SET('Unassigned'))
	status = models.CharField(choices=STATUS_CHOICES, default=PENDING, max_length=150, blank=True)
	priority = models.CharField(choices=PRIORITY_CHOICES, default='Medium', max_length=8, blank=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return f"tickets/bugs/{self.id}"

	class Meta:
		verbose_name = 'bugticket'
		ordering = 	['priority']

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

	class Meta:
		verbose_name = 'newfeatureticket'

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type
