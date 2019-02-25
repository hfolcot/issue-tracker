from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
	total_contributed = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

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