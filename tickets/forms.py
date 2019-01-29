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