from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
	developer = models.BooleanField(default=False)
	rating = models.IntegerField(default=0)

	def __str__(self):
		return f'{self.user.username}'