from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import DeveloperProfile
from . import choices, forms
from .models import BugTicket, NewFeatureTicket

# Create your tests here.

class TestNewBugForm(TestCase):

	def test_form_is_valid(self):
		form = forms.NewBugForm({
			'title' : 'test bug',
			'description' : 'test desc',
			'screenshot' : 'https://s3.eu-west-2.amazonaws.com/issue-tracker-hev/media/images/Capture.PNG'
			})
		self.assertTrue(form.is_valid())

	def test_form_does_not_require_screenshot(self):
		form = forms.NewBugForm({
			'title' : 'test bug',
			'description' : 'test desc',
			'screenshot' : ''
			})
		self.assertTrue(form.is_valid())

	def test_title_desc_cannot_be_blank(self):
		form = forms.NewBugForm({
			'title' : '',
			'description' : '',
			'screenshot' : 'https://s3.eu-west-2.amazonaws.com/issue-tracker-hev/media/images/Capture.PNG'
			})
		self.assertTrue(form.errors['title'], [u'This field is required.'])
		self.assertTrue(form.errors['description'], [u'This field is required.'])

class TestNewFeatureForm(TestCase):

	def test_form_is_valid(self):
		form = forms.NewFeatureForm({
			'title' : 'test feature',
			'description' : 'test desc'
			})
		self.assertTrue(form.is_valid())

	def test_title_desc_cannot_be_blank(self):
		form = forms.NewFeatureForm({
			'title' : '',
			'description' : ''
			})
		self.assertTrue(form.errors['title'], [u'This field is required.'])
		self.assertTrue(form.errors['description'], [u'This field is required.'])

class TestBugUpdateForm(TestCase):

	def setUp(self):
		User.objects.create_user(username='bob')
		BugTicket.objects.create(title='test bug 1', 
			description='test description')
		DeveloperProfile.objects.create(user=User.objects.get(pk=1),
			first_name='bob', 
			last_name='tester')

	def test_bug_can_be_updated(self):
		bug = BugTicket.objects.get(title='test bug 1')
		dev = DeveloperProfile.objects.get(id=1)
		form = forms.BugUpdateForm(instance=bug, initial= {
			'priority' : choices.HIGH, 
			'assigned' : dev, 
			'status' : choices.INPROGRESS,
			'time_spent' : 45
			})
		self.assertTrue(form.is_valid)

	def test_fields_can_be_blank(self):
		bug = BugTicket.objects.get(title='test bug 1')
		form = forms.BugUpdateForm(instance=bug, initial= {
			'priority' : '', 
			'assigned' : '', 
			'status' : '',
			'time_spent' : ''
			})
		self.assertTrue(form.is_valid)

class TestFeatureUpdateForm(TestCase):

	def setUp(self):
		User.objects.create_user(username='bob')
		NewFeatureTicket.objects.create(title='test feature 1', 
			description='test description')
		DeveloperProfile.objects.create(user=User.objects.get(pk=1),
			first_name='bob', 
			last_name='tester')

	def test_feature_can_be_updated(self):
		feature = NewFeatureTicket.objects.get(title='test feature 1')
		dev = DeveloperProfile.objects.get(id=1)
		form = forms.FeatureUpdateForm(instance=feature, initial= {
			'assigned' : dev, 
			'cost' : 80.00, 
			'status' : choices.IMPLEMENTED,
			'time_spent' : 80
			})
		self.assertTrue(form.is_valid)

	def test_fields_can_be_blank(self):
		feature = NewFeatureTicket.objects.get(title='test feature 1')
		form = forms.FeatureUpdateForm(instance=feature, initial= {
			'assigned' : '', 
			'cost' : '', 
			'status' : '',
			'time_spent' : ''
			})
		self.assertTrue(form.is_valid)