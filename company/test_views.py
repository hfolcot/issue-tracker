from django.test import TestCase, Client



class TestViews(TestCase):
	
	def test_about_view_renders_with_anonymous_user(self):
		page = self.client.get('/about')
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "about.html")

	def test_statistics_view_renders_with_anonymous_user(self):
		page = self.client.get('/statistics', follow=True)
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "statistics.html")

	def test_contact_view_renders_with_anonymous_user(self):
		page = self.client.get('/contact')
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "contact.html")

	def test_help_view_renders_with_anonymous_user(self):
		page = self.client.get('/help', follow=True)
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "help.html")