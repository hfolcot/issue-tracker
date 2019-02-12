from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import UserRegistrationForm, UpdateProfilePicture
from tickets.models import BugTicket, NewFeatureTicket

# Create your views here.

def registration_view(request):
	"""
	Register a new user
	"""
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
				return redirect('home')
			else:
				messages.error("Account registration failed")
	else:
		registration_form = UserRegistrationForm()
	return render(request, 'register.html', {'form' : registration_form})

@login_required
def profile_view(request):
	"""
	See the profile page of the user currently logged in
	"""
	if request.user.is_staff:
		bug_tickets = BugTicket.objects.filter(assigned=request.user.developerprofile).exclude(status='Fixed')
		new_features = NewFeatureTicket.objects.filter(assigned=request.user.developerprofile).exclude(status='Implemented')
		fixed_bugs = BugTicket.objects.filter(assigned=request.user.developerprofile.id, status="Fixed")
		completed_features = NewFeatureTicket.objects.filter(assigned=request.user.developerprofile.id, status='Implemented')
	else:
		bug_tickets = BugTicket.objects.filter(customer=request.user).exclude(status='Fixed')
		new_features = NewFeatureTicket.objects.filter(customer=request.user).exclude(status='Implemented')
		fixed_bugs = BugTicket.objects.filter(customer=request.user, status='Fixed')
		completed_features = NewFeatureTicket.objects.filter(customer=request.user, status='Implemented')

	if request.method == 'POST':
		img_upload_form = UpdateProfilePicture(request.POST, request.FILES, instance=request.user.profile)
		if img_upload_form.is_valid():
			img_upload_form.save()
			messages.success(request, "Profile Updated")
			return redirect('profile')

	else:	
		img_upload_form = UpdateProfilePicture()

	#Pagination
	bug_paginator = Paginator(bug_tickets, 10) # Show 10 tickets per page
	feature_paginator = Paginator(new_features, 10) # Show 10 tickets per page
	fixed_bug_paginator = Paginator(fixed_bugs, 10) # Show 10 tickets per page
	completed_feature_paginator = Paginator(completed_features, 10) # Show 10 tickets per page

	page = request.GET.get('page')
	bug_tickets = bug_paginator.get_page(page)
	new_features = feature_paginator.get_page(page)	
	fixed_bugs = fixed_bug_paginator.get_page(page)
	completed_features = completed_feature_paginator.get_page(page)

	context = {'bug_tickets' : bug_tickets, 
		'new_features' : new_features,
		'fixed_bugs': fixed_bugs,
		'completed_features': completed_features, 
		'img_upload_form': img_upload_form
	}
	return render(request, 'profile.html', context)