from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse, redirect

from comments.forms import CommentForm
from comments.models import Comment
from .models import BugTicket, NewFeatureTicket
from .forms import NewBugForm, NewFeatureForm, BugUpdateForm, FeatureUpdateForm

# Create your views here.

def all_tickets_view(request):
	"""
	A home page showing all outstanding tickets
	"""
	bug_tickets = BugTicket.objects.exclude(status='Fixed')
	new_features = NewFeatureTicket.objects.exclude(status='Implemented')
	fixed_bugs = BugTicket.objects.filter(status='Fixed')
	completed_features = NewFeatureTicket.objects.filter(status='Implemented')

	#Search function
	query = request.GET.get('query')
	if query:
		bug_tickets = bug_tickets.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query) |
				Q(customer__first_name__icontains=query) |
				Q(customer__last_name__icontains=query) |
				Q(id__icontains=query)
				).distinct()
			
		new_features = new_features.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query) |
				Q(customer__first_name__icontains=query) |
				Q(customer__last_name__icontains=query) |
				Q(id__icontains=query)
				).distinct()

		fixed_bugs = fixed_bugs.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query) |
				Q(customer__first_name__icontains=query) |
				Q(customer__last_name__icontains=query) |
				Q(id__icontains=query)
				).distinct()
		
		completed_features = completed_features.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query) |
				Q(customer__first_name__icontains=query) |
				Q(customer__last_name__icontains=query) |
				Q(id__icontains=query)
				).distinct()

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

	context = {
		'bug_tickets' : bug_tickets, 
		'new_features' : new_features,
		'fixed_bugs' : fixed_bugs,
		'completed_features' : completed_features

	}		
	return render(request, 'tickets.html', context)

def bug_ticket_view(request, id):
	"""
	Opening the bug ticket to view specifics and add comments
	"""
	bug = get_object_or_404(BugTicket, id=id)
	#Assigning the bug and marking as resolved
	update_form = BugUpdateForm(request.POST or None, instance=bug)
	if update_form.is_valid():
		update_form.save()
		messages.success(request, f"Ticket Updated")

	#Adding a new comment
	initial_data = {
		"content_type": bug.get_content_type,
		"object_id": bug.id
	}
	comment_form = CommentForm(request.POST or None, initial=initial_data)
	if comment_form.is_valid():
		c_type = comment_form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		oid = comment_form.cleaned_data.get("object_id")
		content_data = comment_form.cleaned_data.get("content")
		new_comment, created = Comment.objects.get_or_create(
							user=request.user,
							content_type=content_type,
							object_id=oid,
							content=content_data
							)
		return HttpResponseRedirect(reverse('bug', args=(bug.id,)))
	#Get comments to display
	comments = Comment.get_comments(BugTicket, bug.id)
	
	#Pagination (comments)
	comment_paginator = Paginator(comments, 10) # Show 10 tickets per page
	page = request.GET.get('page')
	comments = comment_paginator.get_page(page)

	#Context
	context = {
		'bug' : bug, 
		'comments' : comments, 
		'comment_form' : comment_form, 
		'update_form' : update_form}
	return render(request, 'bug.html', context)

def new_bug_view(request):
	"""
	Add a new bug ticket to the system
	"""
	new_bug_form = NewBugForm(request.POST or None, request.FILES or None)
	if new_bug_form.is_valid():
		bug = new_bug_form.save()
		bug.customer = request.user
		bug.save()
		return redirect(bug_ticket_view, bug.id)
	return render(request, 'new_ticket.html', {'form' : new_bug_form})

def feature_ticket_view(request, id):
	"""
	Opening the feature ticket to view specifics and add comments
	"""
	feature = get_object_or_404(NewFeatureTicket, id=id)

	#Assigning to a developer, adding a quote and marking as implemented
	update_form = FeatureUpdateForm(request.POST or None, instance=feature)
	if update_form.is_valid():
		updates = update_form.save()
		if updates.cost > 0:
			updates.quoted = True
			updates.save()
		messages.success(request, f"Ticket Updated")

	#Adding a new comment
	initial_data = {
		"content_type": feature.get_content_type,
		"object_id": feature.id
	}
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		oid = form.cleaned_data.get("object_id")
		content_data = form.cleaned_data.get("content")
		new_comment, created = Comment.objects.get_or_create(
							user=request.user,
							content_type=content_type,
							object_id=oid,
							content=content_data
							)
		return HttpResponseRedirect(reverse('feature', args=(feature.id,)))

	#Get comments
	comments = Comment.get_comments(NewFeatureTicket, feature.id)

	#Pagination (comments)
	comment_paginator = Paginator(comments, 10) # Show 10 tickets per page
	page = request.GET.get('page')
	comments = comment_paginator.get_page(page)

	context = {'feature' : feature, 
		'comments' : comments, 
		'comment_form' : form,
		'update_form' : update_form}

	return render(request, 'feature.html', context)

def new_feature_view(request):
	"""
	Add a new feature ticket to the system
	"""
	new_feature_form = NewFeatureForm(request.POST or None, request.FILES or None)
	if new_feature_form.is_valid():
		feature = new_feature_form.save()
		feature.customer = request.user
		feature.save()
		return redirect(feature_ticket_view, feature.id)
	return render(request, 'new_ticket.html', {'form' : new_feature_form})