from django.contrib.auth.models import User
from django.test import TestCase, Client

from tickets.models import NewFeatureTicket


class TestViews(TestCase):

	def test_get_checkout_page(self):
		user = User.objects.create_user('test', 'test@test.test', 'testing321')
		item = NewFeatureTicket.objects.create(title='test', description='test', quoted=True, cost=10.00)
		self.client.login(username='test', password='testing321')
		page = self.client.get('/checkout/{0}'.format(item.id), follow=True)
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "checkout.html")