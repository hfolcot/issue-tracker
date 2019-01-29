from django.shortcuts import render, get_object_or_404
from .models import BugTicket, NewFeatureTicket

# Create your views here.

def all_tickets(request):
	"""
	A home page showing all outstanding tickets
	"""
	bug_tickets = BugTicket.objects.all()
	new_features = NewFeatureTicket.objects.all()
	return render(request, 'tickets.html', {'bug_tickets' : bug_tickets, 'new_features' : new_features})

def bug_ticket(request, id):
	"""
	Opening the ticket to view specifics and add comments
	"""
	bug = get_object_or_404(BugTicket, id=id)
	return render(request, 'bug.html', {'bug' : bug})