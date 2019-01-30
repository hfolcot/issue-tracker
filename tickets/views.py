from django.shortcuts import render, get_object_or_404
from .models import BugTicket, NewFeatureTicket
from .forms import NewBugForm, NewFeatureForm

# Create your views here.

def all_tickets_view(request):
	"""
	A home page showing all outstanding tickets
	"""
	bug_tickets = BugTicket.objects.all()
	new_features = NewFeatureTicket.objects.all()
	return render(request, 'tickets.html', {'bug_tickets' : bug_tickets, 'new_features' : new_features})

def bug_ticket_view(request, id):
	"""
	Opening the ticket to view specifics and add comments
	"""
	bug = get_object_or_404(BugTicket, id=id)
	return render(request, 'bug.html', {'bug' : bug})

def new_bug_view(request):
	"""
	Add a new bug ticket to the system
	"""
	new_bug_form = NewBugForm(request.POST or None, request.FILES or None)
	if new_bug_form.is_valid():
		new_bug_form.save()
	return render(request, 'new_ticket.html', {'form' : new_bug_form})

def new_feature_view(request):
	"""
	Add a new bug ticket to the system
	"""
	new_feature_form = NewFeatureForm(request.POST or None, request.FILES or None)
	if new_feature_form.is_valid():
		new_feature_form.save()
	return render(request, 'new_ticket.html', {'form' : new_feature_form})