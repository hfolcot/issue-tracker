from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=50, null=True)
	last_name = models.CharField(max_length=50, null=True)
	image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
	rating = models.IntegerField(default=0)

	def __str__(self):
		return f'%s %s' % (self.first_name, self.last_name)

	def get_image_url(self):
		return f"{self.image.url}"


class DeveloperProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=50, null=True)
	last_name = models.CharField(max_length=50, null=True)

	def __str__(self):
		return f'%s %s' % (self.first_name, self.last_name)