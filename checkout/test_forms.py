import os

from django.test import TestCase
from . import forms

# Create your tests here.

class TestMakePaymentForm(TestCase):

	def test_payment_form_valid(self):
		stripe = os.environ.get('STRIPE_PUBLISHABLE')
		form = forms.MakePaymentForm({'credit_card_number' : '4242424242424242', 
			'cvv' : '424', 
			'expiry_month' : '12', 
			'expiry_year' : '2038', 
			'stripe_id' : stripe})
		self.assertTrue(form.is_valid())

class TestOrderForm(TestCase):

	def test_can_create_order(self):
		form = forms.OrderForm({'full_name' : 'test test', 
			'phone_number' : '0987765432', 
			'country' : 'UK', 
			'postcode' : 'W12 7RJ', 
			'town_or_city' : 'London', 
			'street_address1' : '1 London Street', 
			'street_address2' : 'London Town', 
			'county' : 'Greater London'})
		self.assertTrue(form.is_valid())
	
	def test_can_create_order_with_blank_postcode(self):
		form = forms.OrderForm({'full_name' : 'test test', 
			'phone_number' : '0987765432', 
			'country' : 'UK', 
			'postcode' : '', 
			'town_or_city' : 'London', 
			'street_address1' : '1 London Street', 
			'street_address2' : 'London Town', 
			'county' : 'Greater London'})
		self.assertTrue(form.is_valid())

	def test_cannot_create_order_with_blank_details(self):
		form = forms.OrderForm({'full_name' : '', 
			'phone_number' : '', 
			'country' : '', 
			'postcode' : '', 
			'town_or_city' : '', 
			'street_address1' : '', 
			'street_address2' : '', 
			'county' : ''})
		self.assertTrue(form.errors['full_name'], [u'This field is required.'])
		self.assertTrue(form.errors['phone_number'], [u'This field is required.'])
		self.assertTrue(form.errors['country'], [u'This field is required.'])
		self.assertTrue(form.errors['town_or_city'], [u'This field is required.'])
		self.assertTrue(form.errors['street_address1'], [u'This field is required.'])
		self.assertTrue(form.errors['street_address2'], [u'This field is required.'])
		self.assertTrue(form.errors['county'], [u'This field is required.'])