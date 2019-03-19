from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Comment

from news.models import Article
from tickets.models import NewFeatureTicket, BugTicket

class TestCommentModel(TestCase):
	def setUp(self):
		User.objects.create_user('test', 'test@test.test', 'testing321')
		User.objects.create_user('test2', 'test2@test.test', 'testing321')
		NewFeatureTicket.objects.create(title='test', description='test', quoted=True, cost=10.00)
		BugTicket.objects.create(title='bugtest', description='bugtest')
		Comment.objects.create(user=User.objects.get(pk=2), 
			content='Test', 
			content_type=NewFeatureTicket.objects.get(pk=1).get_content_type, 
			object_id=1)
		Article.objects.create(title='test article',
			content='test article content')

	def test_comment_user_becomes_sentinel_user_if_user_deleted(self):
		user = User.objects.get(username='test2')
		feature = NewFeatureTicket.objects.get(pk=1)
		comment = Comment.objects.get(pk=1)
		self.assertEqual(comment.user.username, user.username)
		user.delete()
		comment_after_delete = Comment.objects.get(pk=1)
		self.assertEqual(comment_after_delete.user.username, 'deleteduser')

	def test_comment_user_defaults_to_1_if_no_user_given(self):
		feature = NewFeatureTicket.objects.get(pk=1)
		Comment.objects.create(
			content='Test2', 
			content_type=feature.get_content_type, 
			object_id=1)
		comment = Comment.objects.get(content='Test2')
		self.assertEqual(comment.user.id, 1)

	def test_content_types_are_working_on_bugs(self):
		bug = BugTicket.objects.get(pk=1)
		user = User.objects.get(username='test')
		Comment.objects.create(user=user, content='Testbug', content_type=bug.get_content_type, object_id=1)
		bug_comment_ctype = Comment.objects.get(content='Testbug').content_type
		bug_ctype = bug.get_content_type
		self.assertEqual(bug_ctype, bug_comment_ctype)

	def test_content_types_are_working_on_features(self):
		feature = NewFeatureTicket.objects.get(pk=1)
		user = User.objects.get(username='test')
		Comment.objects.create(user=user, content='Testfeature', content_type=feature.get_content_type, object_id=1)
		feature_ctype = feature.get_content_type		
		feature_comment_ctype = Comment.objects.get(content='Testfeature').content_type
		self.assertEqual(feature_ctype, feature_comment_ctype)

	def test_content_types_are_working_on_articles(self):
		article = Article.objects.get(pk=1)
		user = User.objects.get(username='test')
		Comment.objects.create(user=user, content='article', content_type=article.get_content_type, object_id=1)
		article_ctype =article.get_content_type		
		comment_ctype = Comment.objects.get(content='article').content_type
		self.assertEqual(article_ctype, comment_ctype)

	def test_get_comments(self):
		comments = Comment.get_comments(NewFeatureTicket, 1)
		self.assertTrue(len(comments) > 0)