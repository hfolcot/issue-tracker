from django.contrib.auth.models import User
from django.test import TestCase
from . import forms
from tickets.models import BugTicket, NewFeatureTicket



class TestCommentForm(TestCase):
	def setUp(self):
		BugTicket.objects.create(title='test bug', description='test bug')
		NewFeatureTicket.objects.create(title='test feature', description='test feature')
		User.objects.create(username='testuser', password='testing321')

	def test_can_create_comment_on_bug(self):
		bug = BugTicket.objects.get(title='test bug')
		form = forms.CommentForm({'content':'test', 
			'content_type' : bug.get_content_type, 
			'object_id' : bug.id})
		self.assertTrue(form.is_valid())

	def test_can_create_comment_on_feature(self):
		feature = NewFeatureTicket.objects.get(title='test feature')
		form = forms.CommentForm({'content':'test', 
			'content_type' : feature.get_content_type, 
			'object_id' : feature.id})
		self.assertTrue(form.is_valid())