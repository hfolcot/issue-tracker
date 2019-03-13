from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Profile

class UserRegistrationForm(UserCreationForm):
	"""
	New user registration form
	"""

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

	def clean_email(self):
		email = self.cleaned_data.get('email')
		username = self.cleaned_data.get('username')
		if User.objects.filter(email=email).exclude(username=username):
			raise forms.ValidationError(u'Email address must be unique')
		return email

class UpdateProfilePicture(forms.ModelForm):
	"""
	Form to update the user's profile image
	"""
	class Meta:
		model = Profile
		fields = ['image']

class UpdateAboutMeForm(forms.ModelForm):
	"""
	Form to update the user's "about me" section
	"""
	class Meta:
		model = Profile
		fields = ['about']