from django import forms
from django.contrib.auth.models import User
from accounts.models import Profile
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
	assignedto = forms.ModelChoiceField(queryset=Profile.objects.filter(developer=True), 
										empty_label="None", 
										label="Assigned to: ", 
										required = False)

	class Meta:
		model = BugTicket
		fields = ['priority', 'assignedto', 'status']