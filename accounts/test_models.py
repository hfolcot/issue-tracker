from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from checkout.models import Order
from tickets.models import NewFeatureTicket


class TestProfileModel(TestCase):
	def setUp(self):
		User.objects.create_user('test', 'test@test.test', 'testing321')

	def test_profile_created_when_user_created(self):
		user = User.objects.get(username='test')
		self.assertTrue(user.profile)

	def test_image_field_defaults_to_default_pic(self):
		user = User.objects.get(username='test')
		self.assertEqual(user.profile.image, 'profile_pics/default.jpg')

	def test_get_image_url_of_profile(self):
		user = User.objects.get(username='test')
		image_path = user.profile.get_image_url()
		self.assertEqual(image_path, 'https://issue-tracker-hev.s3.amazonaws.com/media/profile_pics/default.jpg')

class TestSentinelUser(TestCase):	
	def setUp(self):
		User.objects.create_user('test', 'test@test.test', 'testing321')
		user = User.objects.get(username='test')
		# Order must be created to trigger get_sentinel_user on deletion of user
		item = NewFeatureTicket.objects.create(title='test', description='test', quoted=True, cost=10.00)
		Order.objects.create(user=user,
			full_name='test test', 
			phone_number='0987765432', 
			country='UK',
			town_or_city='London', 
			street_address1 = '1 London Street', 
			street_address2 = 'London Town', 
			county = 'Greater London',
			date=timezone.now(),
			donation=5.00,
			item=item)

	def test_get_sentinel_user(self):
		user = User.objects.get(username='test')
		user.delete()
		sentinel_user = User.objects.get(username='deleteduser')
		self.assertTrue(sentinel_user)