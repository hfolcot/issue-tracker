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



class BugTicket(models.Model):
	"""
	Model for a ticket describing a bug
	"""
	customer = models.ForeignKey(User, null=True,
        			on_delete=models.CASCADE,)
	title = models.CharField(max_length=100, blank=False)
	description = models.TextField()
	timestamp = models.DateTimeField(auto_now=True)
	screenshot = models.ImageField(upload_to='images', blank=True)
	assigned = models.ForeignKey(DeveloperProfile, default=choices.UNASSIGNED, on_delete=models.SET('Unassigned'))
	status = models.CharField(choices=choices.STATUS_CHOICES, default=choices.PENDING, max_length=150, blank=True)
	priority = models.CharField(choices=choices.PRIORITY_CHOICES, default='Medium', max_length=8, blank=True)
	time_spent = models.IntegerField(default=0)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('bug', kwargs={"id": self.id})

	class Meta:
		verbose_name = 'bugticket'
		ordering = 	['priority']

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type

	@property
	def get_upvotes(self):
		#Retrieve the number of positive votes for the bug
		instance = self
		votes = Vote.get_votes(BugTicket, self.id)
		upvotes = 0
		for vote in votes:
			if vote.positive_vote == True:
				upvotes += 1
		return upvotes	

	@property
	def get_downvotes(self):
		#Retrieve the number of negative votes for the bug
		instance = self
		votes = Vote.get_votes(BugTicket, self.id)
		downvotes = 0
		for vote in votes:
			if vote.positive_vote == False:
				downvotes += 1
		return downvotes

	def get_last_update(self):
		#Get the most recent update timestamp for the specified ticket
		content_type = ContentType.objects.get_for_model(BugTicket)
		oid = self.pk
		try:
			update = Update.objects.filter(content_type=content_type, object_id=oid).order_by('-id')[0]
			update = update.timestamp
		except:
			update = 'Awaiting Response'
		return update

class NewFeatureTicket(models.Model):
	customer = models.ForeignKey(User, null=True,
        			on_delete=models.CASCADE,)
	title = models.CharField(max_length=100, blank=False)
	description = models.TextField()
	assigned = models.ForeignKey(DeveloperProfile, default=choices.UNASSIGNED, on_delete=models.SET('Unassigned'))
	quoted = models.BooleanField(default=False)
	cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
	status = models.CharField(choices=choices.FEATURE_STATUS_CHOICES, default=choices.AWAITINGQUOTE, max_length=150, blank=True)
	time_spent = models.PositiveIntegerField(default=0)
	number_of_donations = models.PositiveIntegerField(default=0)
	total_donations = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
	last_update = models.DateTimeField(null=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('feature', kwargs={"id": self.id})

	class Meta:
		verbose_name = 'newfeatureticket'
		ordering = 	['-quoted']

	@property
	def get_content_type(self):
		#Gets the content type for use by the comments model
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type


	def get_last_update(self):
		#Get the most recent update timestamp for the specified ticket
		content_type = ContentType.objects.get_for_model(NewFeatureTicket)
		oid = self.pk
		try:
			update = Update.objects.filter(content_type=content_type, object_id=oid).order_by('-id')[0]
			update = update.timestamp
		except:
			update = 'Awaiting Response'
		return update

class Update(models.Model):
	"""
	A model for each update on a ticket
	"""
	timestamp = models.DateTimeField()
	object_id = models.PositiveIntegerField()
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	content_object = GenericForeignKey('content_type', 'object_id')