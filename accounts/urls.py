from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from django.urls import path
from .views import registration_view, dashboard_view, other_profile_view

urlpatterns = [
	path('register', registration_view, name="register"),
	path('dashboard', dashboard_view, name="dashboard"),
	path('users/<int:id>', other_profile_view, name='profile'),
	path('logout', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
	path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
	path('reset-password', 
		auth_views.PasswordResetView.as_view(template_name='reset_password.html'), 
		name='reset_password'),
	path('password-reset-done', 
		auth_views.PasswordResetDoneView.as_view(
			template_name='password_reset_done.html'), 
		name='password_reset_done'),	
	path('password-reset-confirm/<uidb64>/<token>/', 
		auth_views.PasswordResetConfirmView.as_view(
			template_name='password_reset_confirm.html'), 
		name='password_reset_confirm'),
	path('password-reset-complete', 
		auth_views.PasswordResetCompleteView.as_view(
			template_name='password_reset_complete.html'), 
		name='password_reset_complete'),

]