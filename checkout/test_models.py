from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Order
from tickets.models import NewFeatureTicket

class TestOrderModel(TestCase):
	def setUp(self):
		User.objects.create_user('test', 'test@test.test', 'testing321')
		NewFeatureTicket.objects.create(title='test', description='test', quoted=True, cost=10.00)
		user = User.objects.get(username='test')
		item = NewFeatureTicket.objects.get(title='test')
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

	def test_order_user_updated_to_sentinel_user_when_user_deleted(self):
		user = User.objects.get(username='test')
		user.delete()
		order = Order.objects.get(pk=1)
		self.assertEqual(order.user.username, 'deleteduser')