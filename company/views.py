from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

import datetime
import os

from accounts.models import DeveloperProfile, Profile
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
	email_address = os.environ.get("COMPANY_EMAIL")
	if request.method == 'POST':
		contact_form = ContactForm(request.POST)
		if contact_form.is_valid():
			from_name = contact_form.cleaned_data['your_name']
			from_email = contact_form.cleaned_data['email']
			message = contact_form.cleaned_data['message']
		try:
			send_mail(from_name, message, from_email, [email_address])
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

	dfilters = request.GET.get('dfilter')
	if dfilters:
		developers = DeveloperProfile.objects.all().exclude(id=1).order_by(dfilters)
		staff_panel_active = True
	else:
		developers = DeveloperProfile.objects.all().exclude(id=1).order_by('-time_spent_on_bugs')
		staff_panel_active = False

	cfilters = request.GET.get('cfilter')
	customers = []
	if User.objects.filter(username='deleteduser'):
		deleted_profile = User.objects.get(username='deleteduser').profile.id
	else:
		deleted_profile=None
	if cfilters:
		for profile in Profile.objects.all().order_by(cfilters)[:10]:
			if not profile.user.is_staff and not profile.id == deleted_profile:
				customers.append(profile)
	else:
		for profile in Profile.objects.all().order_by('-total_contributed')[:10]:
			if not profile.user.is_staff and not profile.id == deleted_profile:
				customers.append(profile)
	print(customers)
	context = {
	'fixed_bugs' : bugs_fixed_today,
	'implemented_features' : features_implemented_today,
	'devs' : developers,
	'customers' : customers,
	'staff_panel_active' : staff_panel_active
	}
	return render(request, 'statistics.html', context)

def help_view(request):
	"""
	Render the help page
	"""
	return render(request, 'help.html')