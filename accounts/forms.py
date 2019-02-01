from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class UserRegistrationForm(UserCreationForm):
	"""
	New user registration form
	"""
	developer = forms.BooleanField(label="Tick this box if you are on the UnicornAttractor developer team!", required=False)

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2', 'developer']

	def clean_email(self):
		email = self.cleaned_data.get('email')
		username = self.cleaned_data.get('username')
		if User.objects.filter(email=email).exclude(username=username):
			raise forms.ValidationError(u'Email address must be unique')
		return email