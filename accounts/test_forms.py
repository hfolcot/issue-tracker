from django.test import TestCase
from . import forms


 
class TestUserRegistrationForm(TestCase):
	
	def test_can_create_user(self):
		form = forms.UserRegistrationForm({'username' : 'test', 
			'first_name' : 'bob', 
			'last_name' : 'tester', 
			'email' : 'bob@bob.bob', 
			'password1' : 'speaker11', 
			'password2' : 'speaker11'})
		self.assertTrue(form.is_valid())

	def test_passwords_must_match_error(self):
		form = forms.UserRegistrationForm({'username' : 'test', 
			'first_name' : 'bob', 
			'last_name' : 'tester', 
			'email' : 'bob@bob.bob', 
			'password1' : 'speaker11', 
			'password2' : 'sergbaer'})
		self.assertTrue(form.errors['password2'], [u'Passwords must match.'])

	def test_username_cannot_be_blank(self):
		form = forms.UserRegistrationForm({'username' : '', 
			'first_name' : 'bob', 
			'last_name' : 'tester', 
			'email' : 'bob@bob.bob', 
			'password1' : 'speaker11', 
			'password2' : 'speaker11'})
		self.assertTrue(form.errors['username'], [u'This field is required.'])

	def test_email_is_valid(self):
		form = forms.UserRegistrationForm({'username' : 'bob', 
			'first_name' : 'bob', 
			'last_name' : 'tester', 
			'email' : 'blank', 
			'password1' : 'speaker11', 
			'password2' : 'speaker11'})
		self.assertTrue(form.errors['email'], [u'Please include an \'@\' in the email address. \'blank\' is missing an \'@\'.'])


class TestUpdateAboutMeForm(TestCase):

	def test_form_is_valid(self):
		form = forms.UpdateAboutMeForm({'about' : 'Hello'})
		self.assertTrue(form.is_valid())

	def test_form_cannot_be_blank(self):
		form = forms.UpdateAboutMeForm({'about' : ''})
		self.assertTrue(form.errors['about'], [u'This field is required.'])