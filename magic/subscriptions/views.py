from django.shortcuts import render, redirect
import datetime
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.http import JsonResponse
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
from .models import Plan, Subscription
@login_required
def plans(request):
    plans = Plan.objects.all()
    return render(request, 'subscriptions/plans.html', {'plans': plans})

def charge(request):
    if request.method == 'POST':
        # Get the card information from the request
        token = request.POST.get('stripeToken')
        email = request.POST.get('stripeEmail')
        print(email)
        # allvariables = request.POST
        # print('this is all variables ------------',allvariables)
        amount = int(float(request.POST.get('amount')))

       

        # Create the charge with the card information and amount
        try:
            charge = stripe.Charge.create(
                amount=amount*100,
                currency='cad',
                source=token,
                description='Premium plan',
                receipt_email=email
            )
            return render(request, 'subscriptions/success.html')
        except stripe.error.CardError as e:
            return render(request, 'subscriptions/fail.html')
    return render(request, 'subscriptions/fail.html')


def subscribe(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    user = request.user
    pay_button = plan.price*100
    return render(request, "subscriptions/checkout.html",{'plan':plan,'user':user, 'pay_button':pay_button})
    # subscription = Subscription(user=user, plan=plan)
    # subscription.start_date = datetime.date.today()
    # subscription.end_date = subscription.start_date + datetime.timedelta(days=365)
    # subscription.save()
    # return redirect('plans')

def cancel(request, subscription_id):
    subscription = Subscription.objects.get(id=subscription_id)
    subscription.cancel()
    return redirect('plans')
