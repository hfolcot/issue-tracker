from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import stripe

from .forms import OrderForm, MakePaymentForm
from .models import Order
from tickets.models import NewFeatureTicket

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET

@login_required
def checkout(request, id):
	feature = get_object_or_404(NewFeatureTicket, pk=id)

	# Calculate the max amount the user should contribute
	orders = Order.objects.filter(item=feature)
	if orders:
		donations = 0
		for order in orders:
			donations += order.donation
			max_amount = round(feature.cost - donations, 2)
	else:
		max_amount = feature.cost

	if request.method == 'POST':
		order_form = OrderForm(request.POST)
		payment_form = MakePaymentForm(request.POST)
		donation = float(request.POST['donation'])

		if order_form.is_valid() and payment_form.is_valid():
			total = donation * 100
			print("total:")
			print(total)
			order = order_form.save(commit=False)
			order.donation = donation
			order.date = timezone.now()
			order.item = feature
			order.save()
			
			try:
				customer = stripe.Charge.create(
					amount = int(total),
					currency = 'GBP',
					description = request.user.email,
					card = payment_form.cleaned_data['stripe_id'],
				)
			except stripe.error.CardError:
				messages.error(request, "Your card was declined")

			if customer.paid:
				messages.success(request, "You have successfully paid")
				return redirect(reverse('home'))
			else:
				messages.error(request, "Unable to take payment")

		else:
			print(payment_form.errors)
			messages.error(request, "We were unable to take a payment with that card")

	else:
		payment_form = MakePaymentForm()
		order_form = OrderForm()

	context = {
		'order_form' : order_form,
		'payment_form' : payment_form,
		'publishable' : settings.STRIPE_PUBLISHABLE,
		'feature' : feature,
		'max_amount' : max_amount
	}

	return render(request, 'checkout.html', context)
