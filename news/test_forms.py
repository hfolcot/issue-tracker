from django.test import TestCase

from .forms import NewArticleForm

# Create your tests here.

class TestNewArticleForm(TestCase):

	def test_can_create_article(self):
		form = NewArticleForm({'title':'test', 
			'content':'test content'})
		self.assertTrue(form.is_valid())

	def test_both_fields_must_be_filled(self):
		form = NewArticleForm({'title':'', 
			'content':''})
		self.assertTrue(form.errors['title'], [u'This field is required.'])
		self.assertTrue(form.errors['content'], [u'This field is required.'])