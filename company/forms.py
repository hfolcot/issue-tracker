from django import forms

class ContactForm(forms.Form):
	your_name = forms.CharField(label='Your name', max_length=100)
	email = forms.EmailField(label='Email Address', required=True)
	message = forms.CharField(label='Message', widget=forms.Textarea(attrs={'rows': '5'}), required=True)