from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from tickets.models import NewFeatureTicket

# Create your models here.

class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	full_name = models.CharField(max_length=50, blank=False)
	phone_number = models.CharField(max_length=20, blank=False)
	country = models.CharField(max_length=40, blank=False)
	postcode = models.CharField(max_length=20, blank=True)
	town_or_city = models.CharField(max_length=40, blank=False)
	street_address1 = models.CharField(max_length=40, blank=False)
	street_address2 = models.CharField(max_length=40, blank=False)
	county = models.CharField(max_length=40, blank=False)
	date = models.DateField()
	donation = models.DecimalField(max_digits=6, decimal_places=2)
	item = models.ForeignKey(NewFeatureTicket, on_delete=models.PROTECT, null=False)

	def __str__(self):
		return "{0} - {1} - {2}".format(self.id, self.date, self.user)
