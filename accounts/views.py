from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

import math

from accounts.models import Profile
from .forms import UserRegistrationForm, UpdateProfilePicture, UpdateAboutMeForm
from tickets.choices import PRIORITY_CHOICES, STATUS_CHOICES, FEATURE_STATUS_CHOICES
from tickets.models import BugTicket, NewFeatureTicket

# Create your views here.


def registration_view(request):
	"""
	Register a new user
	"""
	if request.user.is_authenticated:
		return redirect('dashboard')
	if request.method == "POST":
		registration_form = UserRegistrationForm(request.POST)
		if registration_form.is_valid():
			registration_form.save()
			username = registration_form.cleaned_data.get('username')
			user = auth.authenticate(username=username,
									 password=request.POST['password1'])

			if user:
				auth.login(user=user, request=request)
				messages.success(request, f"Welcome {user}! Your account has been created.")
				return redirect('dashboard')
			else:
				messages.error("Account registration failed")
	else:
		registration_form = UserRegistrationForm()
	return render(request, 'register.html', {'form' : registration_form})

@login_required
def dashboard_view(request):
	"""
	See the dashboard of the logged in user
	"""
	order=request.GET.get('order')
	feature_filter = request.GET.get('feature_filter')
	bug_filter = request.GET.get('bug_filter')

	if feature_filter == 'all_open_tickets' or feature_filter == None:
		features =  NewFeatureTicket.objects.order_by(
				order if order else '-last_update').exclude(status='Implemented')
	else:
		features =  NewFeatureTicket.objects.order_by(
				order if order else '-last_update').filter(
				status=feature_filter)

	if bug_filter == 'all_open_tickets' or bug_filter == None:
		bugs =  BugTicket.objects.order_by(
				order if order else '-last_update').exclude(status='Fixed')
	else:
		bugs =  BugTicket.objects.order_by(
				order if order else '-last_update').filter(
				status=bug_filter)
	profile = request.user.profile

	if request.user.is_staff:
		bug_tickets = bugs.filter(assigned=request.user.developerprofile)
		new_features = features.filter(assigned=request.user.developerprofile)
	else:
		bug_tickets = bugs.filter(
			customer=request.user)
		new_features = features.filter(
			customer=request.user)

	

	#Pagination
	bug_paginator = Paginator(bug_tickets, 10) # Show 10 tickets per page
	feature_paginator = Paginator(new_features, 10) # Show 10 tickets per page

	page = request.GET.get('page')
	bug_tickets = bug_paginator.get_page(page)
	new_features = feature_paginator.get_page(page)

	context = {'bug_tickets' : bug_tickets, 
		'new_features' : new_features,
		'profile' : profile,
		'priorities' : PRIORITY_CHOICES,
		'bug_status' : STATUS_CHOICES,
		'feature_status' : FEATURE_STATUS_CHOICES,
		'bug_filter' : bug_filter,
		'feature_filter': feature_filter
	}
	return render(request, 'dashboard.html', context)


@login_required
def profile_view(request, id):
	"""
	View the profile of a selected user
	"""
	profile = get_object_or_404(Profile, id=id)
	about_form = UpdateAboutMeForm(instance=request.user.profile)
	img_upload_form = UpdateProfilePicture()

	if profile.user.is_staff:
		dev = profile.user.developerprofile
		bug_days = math.floor(dev.time_spent_on_bugs / 1440)
		bug_hours = math.floor((dev.time_spent_on_bugs % 1440) / 60)
		bug_mins = dev.time_spent_on_bugs % 60
		feature_days = math.floor(dev.time_spent_on_features / 1440)
		feature_hours = math.floor((dev.time_spent_on_features % 1440) / 60)
		feature_mins = dev.time_spent_on_features % 60
		total_days = math.floor((dev.time_spent_on_bugs + dev.time_spent_on_features) / 1440)
		total_hours = math.floor(((dev.time_spent_on_bugs + dev.time_spent_on_features) % 1440) / 60)
		total_mins = (dev.time_spent_on_bugs + dev.time_spent_on_features) % 60	
		
		context = {
			'profile' : profile,
			'img_upload_form': img_upload_form,
			'about_form' : about_form,
			'bug_days' : bug_days,
			'bug_mins' : bug_mins,
			'bug_hours' : bug_hours,
			'feature_days' : feature_days,
			'feature_mins' : feature_mins,
			'feature_hours' : feature_hours,
			'total_days' : total_days,
			'total_hours' : total_hours,
			'total_mins' : total_mins
		}
	else:
		
		customers = []
		for name in Profile.objects.all().order_by('-total_contributed'):
			if not name.user.is_staff:
				customers.append(name)
		if profile in customers:
			total_position = customers.index(profile) + 1
		customers = []
		for name in Profile.objects.all().order_by('-times_contributed'):
			if not name.user.is_staff:
				customers.append(name)
		if profile in customers:
			times_position = customers.index(profile) + 1
		context = {
		'profile' 		 : profile,
		'total_position' : total_position,
		'times_position' : times_position,
		'img_upload_form': img_upload_form,
		'about_form' 	 : about_form,
		}
	if request.method == 'POST':
		if 'img' in request.POST:
			img_upload_form = UpdateProfilePicture(request.POST, request.FILES, instance=request.user.profile)
			img_upload_form.save()
			messages.success(request, "Profile Updated")
			return redirect('profile', id=request.user.profile.id)
		if 'about-me' in request.POST:
			about_form = UpdateAboutMeForm(request.POST, instance=request.user.profile)
			about_form.save()
			messages.success(request, "Profile Updated")
			return redirect('profile', id=request.user.profile.id)

	return render(request, 'profile.html', context)