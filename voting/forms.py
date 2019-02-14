from django import forms

class VotingForm(forms.Form):
	object_id = forms.IntegerField(widget=forms.HiddenInput)
	content_type = forms.CharField(widget=forms.HiddenInput)
	vote_type = forms.BooleanField(widget=forms.HiddenInput)
