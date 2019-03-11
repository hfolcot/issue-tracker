from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.db import models

from accounts.models import DeveloperProfile
from comments.models import Comment
from tickets import choices
from voting.models import Vote

# Create your models here.


class TicketUpdate(models.Model):
	"""
	A model for each update on a ticket, used to track activity for statistics
	"""
	timestamp = models.DateTimeField()
	object_id = models.PositiveIntegerField()
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	content_object = GenericForeignKey('content_type', 'object_id')
	time_spent = models.IntegerField(default=0)
	user = models.ForeignKey(User, null=True,
        			on_delete=models.CASCADE,)

	def __str__(self):
		return '{0} - {1} - {2}'.format(self.object_id, self.content_type, self.user)

class BugTicket(models.Model):
	"""
	Model for a ticket describing a bug
	"""
	customer = models.ForeignKey(User, null=True,
        			on_delete=models.CASCADE,)
	title = models.CharField(max_length=100, blank=False)
	description = models.TextField(max_length=999)
	timestamp = models.DateTimeField(auto_now=True)
	screenshot = models.ImageField(upload_to='images', blank=True)
	assigned = models.ForeignKey(DeveloperProfile, default=choices.UNASSIGNED, on_delete=models.SET('Unassigned'))
	status = models.CharField(choices=choices.STATUS_CHOICES, default=choices.PENDING, max_length=150, blank=True)
	priority = models.CharField(choices=choices.PRIORITY_CHOICES, default='Medium', max_length=8, blank=True)
	votes = models.ManyToManyField(Vote, blank=True)
	rating = models.IntegerField(default=0)
	time_spent = models.IntegerField(default=0)
	last_update = models.DateTimeField(null=True)
	fixed_date = models.DateTimeField(null=True, blank=True)
	updates = models.ManyToManyField(TicketUpdate, blank=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('bug', kwargs={"id": self.id})

	class Meta:
		verbose_name = 'bugticket'
		ordering = 	['priority', '-last_update']

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type


class NewFeatureTicket(models.Model):
	customer = models.ForeignKey(User, null=True,
        			on_delete=models.CASCADE,)
	title = models.CharField(max_length=100, blank=False)
	description = models.TextField(max_length=999)
	assigned = models.ForeignKey(DeveloperProfile, default=choices.UNASSIGNED, on_delete=models.SET('Unassigned'))
	quoted = models.BooleanField(default=False)
	cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
	status = models.CharField(choices=choices.FEATURE_STATUS_CHOICES, default=choices.AWAITINGQUOTE, max_length=150, blank=True)
	time_spent = models.PositiveIntegerField(default=0)
	number_of_donations = models.PositiveIntegerField(default=0)
	total_donations = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
	last_update = models.DateTimeField(null=True)
	votes = models.ManyToManyField(Vote, blank=True)
	rating = models.IntegerField(default=0)
	implemented_date = models.DateTimeField(null=True, blank=True)
	updates = models.ManyToManyField(TicketUpdate, blank=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('feature', kwargs={"id": self.id})

	class Meta:
		verbose_name = 'newfeatureticket'
		ordering = 	['-quoted', '-last_update']

	@property
	def get_content_type(self):
		#Gets the content type for use by the comments model
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type


