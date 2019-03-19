from django.test import TestCase
from . import forms

class TestContactForm(TestCase):

	def test_form_is_not_valid_without_all_fields_entered(self):
		form = forms.ContactForm({'your_name':'','email':'', 
			'message' : ''})
		self.assertTrue(form.errors['your_name'], [u'This field is required.'])
		self.assertTrue(form.errors['email'], [u'This field is required.'])
		self.assertTrue(form.errors['message'], [u'This field is required.'])

	def test_email_field_is_validated(self):
		form = forms.ContactForm({'your_name':'test','email':'notanemail', 
			'message' : 'test'})
		self.assertTrue(form.errors['email'], [u'Please include an \'@\' in the email address. \'notanemail\' is missing an \'@\'.'])

	def test_form_is_valid_with_all_fields_entered(self):
		form = forms.ContactForm({'your_name':'test','email':'test@test.test', 
			'message' : 'test'})
		self.assertTrue(form.is_valid())