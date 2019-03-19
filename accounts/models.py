from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import models

from voting.models import Vote

# Create your models here.

def get_sentinel_user():
	#return 'deleted' on comments associated with deleted user accounts
    return get_user_model().objects.get_or_create(username='deleteduser', first_name='(Deleted', last_name='user)')[0]



class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics')
	votes = models.ManyToManyField(Vote)
	about = models.TextField(max_length=256, default="This user has not updated this section yet")
	total_contributed = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
	times_contributed = models.IntegerField(default=0)

	def __str__(self):
		return str(self.user)

	def get_image_url(self):
		return f"{self.image.url}"


class DeveloperProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=50, null=True)
	last_name = models.CharField(max_length=50, null=True)
	time_spent_on_bugs = models.IntegerField(default=0)
	time_spent_on_features = models.IntegerField(default=0)

	def __str__(self):
		return f'%s %s' % (self.first_name, self.last_name)