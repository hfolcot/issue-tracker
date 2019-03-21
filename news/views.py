from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse, redirect

from accounts.models import Profile
from comments.forms import CommentForm
from comments.models import Comment
from .models import Article
from .forms import NewArticleForm

# Create your views here.

def blog_list_view(request):
	all_articles = Article.objects.all()
	return render(request, 'news.html', {'articles' : all_articles})

def article_view(request, id):
	article = get_object_or_404(Article, id=id)
	profile = get_object_or_404(Profile, user=article.author)

	#Adding a new comment
	initial_data = {
		"content_type": article.get_content_type,
		"object_id": article.id
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
		return HttpResponseRedirect(reverse('article', args=(article.id,)))
	#Get comments to display
	comments = Comment.get_comments(Article, article.id)
	#Pagination (comments)
	comment_paginator = Paginator(comments, 10) # Show 10 tickets per page
	page = request.GET.get('page')
	comments = comment_paginator.get_page(page)
	context = {
		'article': article, 
		'profile': profile, 
		'comments': comments, 
		'comment_form':comment_form
	}

	return render(request, 'article.html', context)

@login_required
def new_edit_article_view(request, id=None):
	if not request.user.is_staff:
		return redirect('news')
	else:
		article = get_object_or_404(Article, id=id) if id else None
		if request.method == 'POST':
			if article:
				form = NewArticleForm(request.POST, instance=article)
			else:
				form = NewArticleForm(request.POST)
			if form.is_valid():
				article = form.save()
				return redirect(article_view, article.id)
		else:
			form = NewArticleForm(instance=article)
		return render(request, 'new_article.html', {'form':form})