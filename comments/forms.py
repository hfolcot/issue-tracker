from django import forms
from .models import Comment

class CommentForm(forms.Form):
	content_type = forms.CharField(widget=forms.HiddenInput)
	object_id = forms.IntegerField(widget=forms.HiddenInput)
	content = forms.CharField(widget=forms.Textarea(attrs={'rows': '5'}), label='', required=False)
