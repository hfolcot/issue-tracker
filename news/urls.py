from django.urls import path
from .views import blog_list_view, article_view, new_edit_article_view


urlpatterns = [
	path('all', blog_list_view, name="news"),
	path('<int:id>', article_view, name="article"),
	path('add', new_edit_article_view, name="new_article"),
	path('edit/<int:id>', new_edit_article_view, name="edit_article"),
]