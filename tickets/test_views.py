from django.contrib.auth.models import User
from django.test import TestCase, Client


from .models import BugTicket, NewFeatureTicket

from accounts.models import DeveloperProfile

class TestViews(TestCase):
	def setUp(self):
		User.objects.create_user('test', 'test@test.test', 'testing321')
		devuser = DeveloperProfile.objects.create(user=User.objects.get(pk=1))
		BugTicket.objects.create(customer=User.objects.get(pk=1),
			title='Test Bug',
			description='Test description',
			assigned=devuser)
		NewFeatureTicket.objects.create(customer=User.objects.get(pk=1),
			title='Test Feature',
			description='Test description',
			assigned=devuser)

	def test_get_all_tickets_page_unauthenticated(self):
		page = self.client.get('/')
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "tickets.html")

	def test_get_all_tickets_page_authenticated(self):
		user = User.objects.get(pk=1)
		self.client.login(username='test', password='testing321')
		page = self.client.get('/')
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "tickets.html")

	def test_get_bug_ticket_page(self):
		user = User.objects.get(pk=1)
		self.client.login(username='test', password='testing321')
		bug = BugTicket.objects.get(pk=1)
		page = self.client.get('/tickets/bugs/{0}'.format(bug.id), follow=True)
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "bug.html")

	def test_cannot_access_bug_without_authentication(self):
		bug = BugTicket.objects.get(pk=1)
		page = self.client.get('/tickets/bugs/{0}'.format(bug.id), follow=True)
		self.assertRedirects(page, '/accounts/login?next=/tickets/bugs/1')

	def test_get_feature_ticket_page(self):
		user = User.objects.get(pk=1)
		self.client.login(username='test', password='testing321')
		feature = NewFeatureTicket.objects.get(pk=1)
		page = self.client.get('/tickets/features/{0}'.format(feature.id), follow=True)
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "feature.html")

	def test_cannot_access_feature_without_authentication(self):
		feature = NewFeatureTicket.objects.get(pk=1)
		page = self.client.get('/tickets/features/{0}'.format(feature.id), follow=True)
		self.assertRedirects(page, '/accounts/login?next=/tickets/features/1')

	def test_get_new_bug_page(self):
		user = User.objects.get(pk=1)
		self.client.login(username='test', password='testing321')
		page = self.client.get('/tickets/bugs/new')
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "new_ticket.html")

	def test_cannot_access_new_bug_page_without_authentication(self):
		page = self.client.get('/tickets/bugs/new')
		self.assertRedirects(page, '/accounts/login?next=/tickets/bugs/new')

	
	def test_get_new_feature_page(self):
		user = User.objects.get(pk=1)
		self.client.login(username='test', password='testing321')
		page = self.client.get('/tickets/features/new')
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "new_ticket.html")

	def test_cannot_access_new_feature_page_without_authentication(self):
		page = self.client.get('/tickets/features/new')
		self.assertRedirects(page, '/accounts/login?next=/tickets/features/new')

