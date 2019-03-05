from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse, redirect
from rest_framework import viewsets, permissions

import datetime
import math

from accounts.models import DeveloperProfile
from checkout.models import Order
from comments.forms import CommentForm
from comments.models import Comment
from .models import BugTicket, NewFeatureTicket, TicketUpdate
from .forms import NewBugForm, NewFeatureForm, BugUpdateForm, FeatureUpdateForm
from .serializers import BugSerializer, FeatureSerializer, TicketUpdateSerializer
from voting.models import Vote

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
	Opening the bug ticket to view specifics and add 
	comments/update/vote.
	All users can vote and comment but only those with
	staff access can update the status, priority and 
	assigned fields.
	"""
	bug = get_object_or_404(BugTicket, id=id)
	user = request.user
	#Initial data for forms
	initial_data = {
		"content_type": bug.get_content_type,
		"object_id": bug.id
	}
	bug_data = {
		'priority' : bug.priority,
		'assigned' : bug.assigned,
		'status' : bug.status,
		'time_spent' : 0
	}
	
	if request.method == 'POST':
	#Assigning the bug, adding time spent and marking as resolved
	#Staff only
		if 'update' in request.POST:
			update_form = BugUpdateForm(request.POST, instance=bug)
			time_spent = bug.time_spent + int(request.POST['time_spent'])
			if update_form.is_valid():
				updated_bug = update_form.save()
				updated_bug.time_spent = time_spent
				updated_bug.last_update = datetime.datetime.now()
				if updated_bug.status == 'Fixed':
					updated_bug.fixed_date = datetime.datetime.now()
				updated_bug.save()
				dev = get_object_or_404(DeveloperProfile, user=user.id)
				dev.time_spent_on_bugs = F('time_spent_on_bugs') + int(request.POST['time_spent'])
				dev.save()
				TicketUpdate.objects.get_or_create(
					timestamp = datetime.datetime.now(),
					object_id = bug.id,
					content_type = bug.get_content_type,
					time_spent = int(request.POST['time_spent']),
					user = request.user
					)
				messages.success(request, f"Ticket Updated")
				return HttpResponseRedirect(reverse('bug', args=(bug.id,)))
			else:
				messages.error(request, f"There was a problem")
				return HttpResponseRedirect(reverse('bug', args=(bug.id,)))

	#Commenting
	#All Users
		elif 'comment' in request.POST:
			comment_form = CommentForm(request.POST, initial=initial_data)
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
				TicketUpdate.objects.get_or_create(
					timestamp = datetime.datetime.now(),
					object_id = bug.id,
					content_type = bug.get_content_type,
					user = request.user
					)
				bug.last_update = datetime.datetime.now()
				bug.save()

			return HttpResponseRedirect(reverse('bug', args=(bug.id,)))

	#Voting (All Users)
		elif 'upvote' in request.POST:
			new_vote, created = Vote.objects.get_or_create(
					positive_vote=True,
					user=request.user,
					object_id=bug.id,
					content_type=bug.get_content_type
						)
			user.profile.votes.add(new_vote)
			bug.votes.add(new_vote)
			bug.rating = F('rating') + 1
			bug.save()
			messages.success(request, f'Thanks for voting')
			return HttpResponseRedirect(reverse('bug', args=(bug.id,)))
		elif 'downvote' in request.POST:
			new_vote, created = Vote.objects.get_or_create(
					positive_vote=False,
					user=request.user,
					object_id=bug.id,
					content_type=bug.get_content_type
						)
			user.profile.votes.add(new_vote)
			bug.votes.add(new_vote)
			bug.rating = F('rating') - 1
			bug.save()
			messages.success(request, f'Thanks for voting')
			return HttpResponseRedirect(reverse('bug', args=(bug.id,)))
	else:
		#Blank forms:
		update_form = BugUpdateForm(initial=bug_data)
		comment_form = CommentForm(initial=initial_data)

		#Current Information on Bug
		hours_worked_on = math.floor(bug.time_spent/60)
		mins_worked_on = bug.time_spent%60

		#Retrieve the votes for the specific bug
		upvotes_list = bug.votes.filter(positive_vote=True)
		upvotes = upvotes_list.count()
		downvotes_list = bug.votes.filter(positive_vote=False)
		downvotes = downvotes_list.count()

		#check if user has already voted
		user_votes = user.profile.votes.all()
		bug_votes = bug.votes.all()
		print(user_votes)
		print(bug_votes)
		if bug_votes and user_votes:
			for vote in bug_votes:
				if vote in user_votes:
					user_voted = True
					break
				else:
					user_voted = False
		else:
			user_voted = False


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
			'update_form' : update_form,
			'hours' : hours_worked_on,
			'mins' : mins_worked_on,
			'user_voted' : user_voted,
			'upvotes' : upvotes,
			'downvotes' : downvotes
			}
	return render(request, 'bug.html', context)


def new_bug_view(request):
	"""
	Add a new bug ticket to the system
	"""
	new_bug_form = NewBugForm(request.POST or None, request.FILES or None)
	if new_bug_form.is_valid():
		bug = new_bug_form.save()
		bug.customer = request.user
		bug.last_update = datetime.datetime.now()
		bug.save()
		return redirect(bug_ticket_view, bug.id)
	context = {
		'form' : new_bug_form,
		'title' : 'New Bug Report',
		'caption' : 'Any bugs reported will be fixed for free.'
	}
	return render(request, 'new_ticket.html', context)

def feature_ticket_view(request, id):
	"""
	Opening the feature ticket to view specifics and add comments
	"""
	feature = get_object_or_404(NewFeatureTicket, id=id)
	user = request.user

	#Initial data for forms
	comment_data = {
		"content_type": feature.get_content_type,
		"object_id": feature.id
	}
	feature_data = {
		'cost' : feature.cost,
		'assigned' : feature.assigned,
		'status' : feature.status,
		'time_spent' : 0
	}
	if request.method == 'POST':
		if 'update' in request.POST:
		#Assigning to a developer, adding a quote and marking as implemented
		#Staff only
			update_form = FeatureUpdateForm(request.POST, instance=feature)
			time_spent = feature.time_spent + int(request.POST['time_spent'])
			dev = get_object_or_404(DeveloperProfile, user=user.id)
			if update_form.is_valid():
				updated_feature = update_form.save()
				updated_feature.last_update = datetime.datetime.now()
				updated_feature.time_spent = time_spent
				if updated_feature.cost > 0:
					updated_feature.quoted = True
				if updated_feature.status == 'Implemented':
					updated_feature.implemented_date = datetime.datetime.now()
				updated_feature.save()
				dev.time_spent_on_features = F('time_spent_on_features') + int(request.POST['time_spent'])
				dev.save()
				TicketUpdate.objects.get_or_create(
					timestamp = datetime.datetime.now(),
					object_id = feature.id,
					content_type = feature.get_content_type,
					time_spent = int(request.POST['time_spent']),
					user = request.user
					)
				messages.success(request, f"Ticket Updated")
			return HttpResponseRedirect(reverse('feature', args=(feature.id,)))
		elif 'comment' in request.POST:
			#Adding a new comment
			#All Users
			form = CommentForm(request.POST)
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

	#Voting (All Users)
		elif 'upvote' in request.POST:
			new_vote, created = Vote.objects.get_or_create(
					positive_vote=True,
					user=request.user,
					object_id=feature.id,
					content_type=feature.get_content_type
						)
			user.profile.votes.add(new_vote)
			feature.votes.add(new_vote)
			feature.rating = F('rating') + 1
			feature.save()
			messages.success(request, f'Thanks for voting')
			return HttpResponseRedirect(reverse('feature', args=(feature.id,)))
		elif 'downvote' in request.POST:
			new_vote, created = Vote.objects.get_or_create(
					positive_vote=False,
					user=request.user,
					object_id=feature.id,
					content_type=feature.get_content_type
						)
			user.profile.votes.add(new_vote)
			feature.votes.add(new_vote)
			feature.rating = F('rating') - 1
			feature.save()
			messages.success(request, f'Thanks for voting')
			return HttpResponseRedirect(reverse('feature', args=(feature.id,)))
	else:
		#Initial Forms
		update_form = FeatureUpdateForm(initial=feature_data)
		comment_form = CommentForm(initial = comment_data)

		# Calculate the feature details
		donations = feature.total_donations
		percentage = round((donations / feature.cost)*100, 0)
		remaining = round(feature.cost - donations, 2)
		hours_worked_on = math.floor(feature.time_spent/60)
		mins_worked_on = feature.time_spent%60

		#Retrieve the number votes for the specific feature
		upvotes_list = feature.votes.filter(positive_vote=True)
		upvotes = upvotes_list.count()
		downvotes_list = feature.votes.filter(positive_vote=False)
		downvotes = downvotes_list.count()

		#check if user has already voted
		user_votes = user.profile.votes.all()
		feature_votes = feature.votes.all()
		if feature_votes:
			for vote in feature_votes:
				if vote in user_votes:
					user_voted = True
					break
				else:
					user_voted = False
		else:
			user_voted = False

		#Get comments
		comments = Comment.get_comments(NewFeatureTicket, feature.id)

		#Pagination (comments)
		comment_paginator = Paginator(comments, 10) # Show 10 tickets per page
		page = request.GET.get('page')
		comments = comment_paginator.get_page(page)

		#Context
		context = {'feature' : feature, 
			'comments' : comments, 
			'comment_form' : comment_form,
			'update_form' : update_form,
			'donations' : donations,
			'percentage' : percentage,
			'remaining' : remaining,
			'hours' : hours_worked_on,
			'mins' : mins_worked_on,
			'upvotes' : upvotes,
			'downvotes': downvotes,
			'user_voted' : user_voted}

		return render(request, 'feature.html', context)

def new_feature_view(request):
	"""
	Add a new feature ticket to the system
	"""
	new_feature_form = NewFeatureForm(request.POST or None, request.FILES or None)
	if new_feature_form.is_valid():
		feature = new_feature_form.save()
		feature.customer = request.user
		feature.last_update = datetime.datetime.now()
		feature.save()
		return redirect(feature_ticket_view, feature.id)
	context = {
		'form' : new_feature_form,
		'title' : "Suggest a New Feature",
		'caption' : "Ideas will be quoted and contributions can then be made towards implementing."
	}
	return render(request, 'new_ticket.html', context)

class BugTicketApiView(viewsets.ModelViewSet):
	queryset = BugTicket.objects.all()
	serializer_class = BugSerializer

class FeatureTicketApiView(viewsets.ModelViewSet):
	queryset = NewFeatureTicket.objects.all()
	serializer_class = FeatureSerializer

class TicketUpdateApiView(viewsets.ModelViewSet):
	queryset = TicketUpdate.objects.all()
	serializer_class = TicketUpdateSerializer