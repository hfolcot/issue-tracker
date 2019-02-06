from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse

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

	return render(request, 'article.html', {'article': article, 'profile': profile, 'comments': comments, 'comment_form':comment_form})

def new_article_view(request):
	form = NewArticleForm(request.POST or None)
	if form.is_valid():
		form.save()
	return render(request, 'new_article.html', {'form':form})