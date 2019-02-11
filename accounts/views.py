from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
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
	bug_tickets = BugTicket.objects.all()
	new_features = NewFeatureTicket.objects.all()
	if request.method == 'POST':
		img_upload_form = UpdateProfilePicture(request.POST, request.FILES, instance=request.user.profile)
		if img_upload_form.is_valid():
			img_upload_form.save()
			messages.success(request, "Profile Updated")
			return redirect('profile')

	else:	
		img_upload_form = UpdateProfilePicture()
	context = {'bugs' : bug_tickets, 
		'features' : new_features, 
		'img_upload_form': img_upload_form
	}
	return render(request, 'profile.html', context)