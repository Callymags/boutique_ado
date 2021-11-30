from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag: 
        messages.error(request, "There's nothing in your bag at the moment")
        # Prevents people from manually accessing url by typing /checkout 
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51K1H5NLBL4yEJjCGHqScN1wu2zAOGKU3wroLEPurTDSWXsEd5m1edvpOokiS1R1KmrOnPzENDAIvzL71PUEKr69C007ArPoGrw',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
