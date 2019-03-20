from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F
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
	current_total = float(feature.total_donations)
	max_amount = feature.cost - feature.total_donations

	if request.method == 'POST':
		order_form = OrderForm(request.POST)
		payment_form = MakePaymentForm(request.POST)
		donation = float(request.POST['donation'])
		

		if order_form.is_valid() and payment_form.is_valid():
			total = donation * 100
			order = order_form.save(commit=False)
			order.donation = donation
			order.date = timezone.now()
			order.item = feature
			order.user = request.user
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
				messages.success(request, "Thank you for your contribution!")
				feature.number_of_donations = F('number_of_donations') + 1
				feature.total_donations = F('total_donations') + donation
				total_donated = current_total + donation
				if int(total_donated) == int(feature.cost):
					feature.status = 'In Progress'
				feature.save()
				request.user.profile.total_contributed = F('total_contributed') + donation
				request.user.profile.times_contributed = F('times_contributed') + 1
				request.user.profile.save()
				return redirect(reverse('feature', args=(feature.id,)))
			else:
				messages.error(request, "Unable to take payment")

		else:
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
