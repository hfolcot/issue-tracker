from django.db import models

# Create your models here.

class BugTicket(models.Model):
	title = models.CharField(max_length=300, blank=False)
	description = models.TextField()
	screenshot = models.ImageField(upload_to='images')
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
	fixed = models.BooleanField(default=False)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return f"tickets/bugs/{self.id}"

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