from django.contrib.auth.models import User
from django.test import TestCase

from .models import Article

# Create your tests here.


class TestViews(TestCase):
	def setUp(self):
		User.objects.create_user('test', 'test@test.test', 'testing321')
		User.objects.create_superuser('admin', 'admin@admin.get', 'testing321')
		user = User.objects.get(pk=1)
		Article.objects.create(title='test', content='test', author=user)

	def test_get_blog_list_page(self):
		page = self.client.get('/blog/all')
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "news.html")

	def test_get_article_page(self):
		article = Article.objects.get(pk=1)
		page = self.client.get('/blog/{0}'.format(article.id))
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "article.html")

	def test_get_new_article_page(self):
		self.client.login(username='admin', password='testing321')
		page = self.client.get('/blog/add')
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "new_article.html")

	def test_get_edit_article_page(self):
		self.client.login(username='admin', password='testing321')
		article = Article.objects.get(pk=1)
		page = self.client.get('/blog/edit/{0}'.format(article.id))
		self.assertEqual(page.status_code, 200)
		self.assertTemplateUsed(page, "new_article.html")

	def test_get_new_article_page_when_not_staff(self):
		self.client.login(username='test', password='testing321')
		page = self.client.get('/blog/add')
		self.assertRedirects(page, '/blog/all')

	def test_get_edit_article_page_when_not_staff(self):
		self.client.login(username='test', password='testing321')
		article = Article.objects.get(pk=1)
		page = self.client.get('/blog/edit/{0}'.format(article.id))
		self.assertRedirects(page, '/blog/all')

	def test_get_new_article_page_when_not_logged_in(self):
		page = self.client.get('/blog/add')
		self.assertRedirects(page, '/accounts/login?next=/blog/add')

	def test_get_edit_article_page_when_not_logged_in(self):
		article = Article.objects.get(pk=1)
		page = self.client.get('/blog/edit/{0}'.format(article.id))
		self.assertRedirects(page, '/accounts/login?next=/blog/edit/{0}'.format(article.id))