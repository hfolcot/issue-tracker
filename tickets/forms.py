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
		fields = [
			'priority', 
			'assigned', 
			'status',
			'time_spent'
		]
		labels = {
			'time_spent' : 'Time Spent (mins)'
		}

class FeatureUpdateForm(forms.ModelForm):
	class Meta:
		model = NewFeatureTicket
		fields = [
			'assigned', 
			'cost', 
			'status',
			'time_spent'
		]
		labels = {
			'time_spent' : 'Time Spent (mins)'
		}
