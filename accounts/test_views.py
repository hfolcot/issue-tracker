from django.contrib.auth.models import User
from django.test import TestCase, Client



class TestViews(TestCase):
	def setUp(self):
		User.objects.create_user('test', 'test@test.test', 'testing321')

	def test_get_login_page(self):
		page = self.client.get('/accounts/login')
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "login.html")

	def test_get_logout_page(self):
		page = self.client.get('/accounts/logout')
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "logout.html")

	def test_get_register_page(self):
		page = self.client.get('/accounts/register')
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "register.html")

	def test_get_profile_page(self):
		user = User.objects.get(username='test')
		profile = user.profile
		self.client.login(username='test', password='testing321')
		page = self.client.get('/accounts/users/{0}'.format(profile.id))
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "profile.html")

	def test_get_profile_page_unauthenticated(self):
		user = User.objects.get(username='test')
		profile = user.profile
		page = self.client.get('/accounts/users/{0}'.format(profile.id))
		self.assertRedirects(page, '/accounts/login?next=/accounts/users/{0}'.format(profile.id))

	def test_get_dashboard_page(self):
		user = User.objects.get(username='test')
		self.client.login(username='test', password='testing321')
		page = self.client.get('/accounts/dashboard')
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "dashboard.html")

	def test_get_profile_page_for_nonexistent_user(self):
		user = User.objects.get(username='test')
		self.client.login(username='test', password='testing321')
		page = self.client.get('/accounts/users/9')
		self.assertEqual(page.status_code, 404)
		self.assertTemplateUsed(page, "404.html")