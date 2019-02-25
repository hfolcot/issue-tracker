"""issuetracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.urls import path
from accounts import urls as accounts_urls
from checkout import urls as checkout_urls
from company.views import about_view, contact_view
from news import urls as blog_urls
from tickets import urls as tickets_urls
from tickets.views import all_tickets_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', all_tickets_view, name='home'),
    path('tickets/', include(tickets_urls)),
    path('accounts/', include(accounts_urls)),
    path('blog/', include(blog_urls)),
    path('about', about_view, name='about'),
    path('contact', contact_view, name='contact'),
    path('checkout/', include(checkout_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)