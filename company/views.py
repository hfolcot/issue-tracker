from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import ContactForm

# Create your views here.

def about_view(request):
	"""
	Render the about page
	"""
	return render(request, 'about.html')

def contact_view(request):
	"""
	Handle the contact form
	"""
	if request.method == 'POST':
		contact_form = ContactForm(request.POST)
		if contact_form.is_valid():
			from_name = contact_form.cleaned_data['your_name']
			from_email = contact_form.cleaned_data['email']
			message = contact_form.cleaned_data['message']
		try:
			send_mail(from_name, message, from_email, ['issuetrackerhev@gmail.com'])
		except BadHeaderError:
			return HttpResponse('Invalid header found.')
		messages.success(request, f"Message sent!")
		return redirect('contact')
	else:
		contact_form = ContactForm()

	context = {
		'contact_form' : contact_form
	}
	return render(request, 'contact.html', context)