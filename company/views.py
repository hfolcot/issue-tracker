from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

import datetime

from accounts.models import DeveloperProfile
from tickets.models import BugTicket, NewFeatureTicket
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

def statistics_view(request):
	"""
	View statistics page
	"""
	today = datetime.date.today()
	bugs_fixed_today = BugTicket.objects.filter(fixed_date__startswith=today)
	features_implemented_today = NewFeatureTicket.objects.filter(implemented_date__startswith=today)
	developers_features = DeveloperProfile.objects.all().exclude(id=1).order_by('-time_spent_on_features')
	developers_bugs = DeveloperProfile.objects.all().exclude(id=1).order_by('-time_spent_on_bugs')
	print(developers_features)
	context = {
	'fixed_bugs' : bugs_fixed_today,
	'implemented_features' : features_implemented_today,
	'devs_by_bugs' : developers_bugs,
	'devs_by_features' : developers_features
	}
	return render(request, 'statistics.html', context)