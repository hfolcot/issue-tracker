from django.urls import path
from .views import checkout

urlpatterns = [
    path('<int:id>/', checkout, name='checkout'),
     ]