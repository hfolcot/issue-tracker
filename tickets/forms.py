from django import forms
from .models import BugTicket, NewFeatureTicket

class NewBugForm(forms.ModelForm):
	class Meta:
		model = BugTicket
		fields = [
			'title',
			'description',
			'screenshot',
		]

class NewFeatureForm(forms.ModelForm):
	class Meta:
		model = NewFeatureTicket
		fields = [
			'title',
			'description',
		]

class BugUpdateForm(forms.ModelForm):
	class Meta:
		model = BugTicket
		fields = ['priority', 'assigned', 'status']

class FeatureUpdateForm(forms.ModelForm):
	class Meta:
		model = NewFeatureTicket
		fields = ['assigned', 'quoted', 'cost', 'status']