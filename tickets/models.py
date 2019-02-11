from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.db import models

from accounts.models import DeveloperProfile
from comments.models import Comment
from tickets import choices

# Create your models here.



class BugTicket(models.Model):
	"""
	Model for a ticket describing a bug
	"""
	customer = models.ForeignKey(User, null=True,
        			on_delete=models.CASCADE,)
	title = models.CharField(max_length=300, blank=False)
	description = models.TextField()
	timestamp = models.DateTimeField(auto_now=True)
	screenshot = models.ImageField(upload_to='images', blank=True)
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	assigned = models.ForeignKey(DeveloperProfile, default=choices.UNASSIGNED, on_delete=models.SET('Unassigned'))
	status = models.CharField(choices=choices.STATUS_CHOICES, default=choices.PENDING, max_length=150, blank=True)
	priority = models.CharField(choices=choices.PRIORITY_CHOICES, default='Medium', max_length=8, blank=True)

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

	def get_last_comment(ticket_type, ticket_id):
		#Get the most recent comment timestamp for the specified ticket
		content_type = ContentType.objects.get_for_model(ticket_type)
		oid = ticket_id
		comment = Comment.objects.filter(content_type=content_type, object_id=oid).order_by('-id')[0]
		return comment

class NewFeatureTicket(models.Model):
	customer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True,
    			on_delete=models.CASCADE,)
	title = models.CharField(max_length=300, blank=False)
	description = models.TextField()
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	assigned = models.ForeignKey(DeveloperProfile, default=choices.UNASSIGNED, on_delete=models.SET('Unassigned'))
	quoted = models.BooleanField(default=False)
	cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
	status = models.CharField(choices=choices.FEATURE_STATUS_CHOICES, default=choices.AWAITINGQUOTE, max_length=150, blank=True)
	contributions = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('feature', kwargs={"id": self.id})

	class Meta:
		verbose_name = 'newfeatureticket'
		ordering = 	['-contributions']

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type
