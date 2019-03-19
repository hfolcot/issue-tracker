from django.contrib.auth.models import User
from django.test import TestCase

from .models import Article

class TestArticle(TestCase):

	def setUp(self):
		User.objects.create_superuser('admintest', 'test@test.test', 'testing321')
		User.objects.create_user('usertest', 'usertest@test.test', 'testing321')
		Article.objects.create(title='New article', content='Some content')

	def test_default_author_1(self):
		article = Article.objects.create(title='New article 2', content='')
		self.assertTrue(article.author, 'admintest')

	def test_get_absolute_url(self):
		article = Article.objects.get(pk=1)
		absolute_url = article.get_absolute_url()
		self.assertEqual(absolute_url, '1')

	def test_article_updated_with_sentinel_user_when_user_deleted(self):
		article = Article.objects.get(pk=1)
		user = User.objects.get(pk=1)
		self.assertEqual(article.author, user)
		user.delete()
		article = Article.objects.get(pk=1)
		self.assertEqual(article.author.username, 'deleteduser')