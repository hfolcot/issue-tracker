from django.shortcuts import render

# Create your views here.

def all_tickets(request):
	"""
	A home page showing all outstanding tickets
	"""
	return render(request, 'tickets.html')