from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect
import stripe
import json
from django.http import JsonResponse, HttpResponse
from djstripe.models import Product
import djstripe
import os
from .models import Subscription, PortalSession
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


@login_required
def checkout(request):
  # Prices = stripe.Price.list()
  products = stripe.Product.list()
  pro = {}
  for product in products:
    prices = stripe.Price.list(product=product.id)
    
    context = {
          'product': product,
          'prices': prices['data']
      }
  return render(request,"subscriptions/checkout.html",context)


def create_checkout_session(request):
    if request.method == 'POST':
        # Reads application/json and returns a response
        lookup_key=request.POST.get('lookup_key'),
        try:  
          prices = stripe.Price.list(
              lookup_keys=lookup_key,
              expand=['data.product']
          )

          checkout_session = stripe.checkout.Session.create(
              line_items=[
                  {
                      'price': prices.data[0].id,
                      'quantity': 1,
                  },
              ],
              mode='subscription',
              success_url="http://localhost:8000/plans/success/",
              cancel_url="http://localhost:8000/plans/cancel",
              
          )
          
          session = stripe.checkout.Session.retrieve(checkout_session.id)
          checkout_session_id = session['id']
          payment_status = session['payment_status']
          subscription = Subscription.objects.filter(user=request.user).exists()
          if not subscription:
            subscription_obj = Subscription.objects.create(user=request.user, checkouts_session_id=checkout_session_id,active=True)
            subscription_obj.save()
          else:
            subscription_obj = Subscription.objects.filter(user=request.user).first()
            checkout_session_id = subscription_obj.checkouts_session_id
            checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
          # return redirect(portalSession.url, code=303)
          return redirect(checkout_session.url, code=303)
        except Exception as e:
            print(e)
    return "Server error", 500

def create_portal_session(request):
  if request.method == "GET":
    # For demonstration purposes, we're using the Checkout session to retrieve the customer ID.
    # Typically this is stored alongside the authenticated user in your database.
    subscription_obj = Subscription.objects.filter(user=request.user).first()
    checkout_session_id = subscription_obj.checkouts_session_id
    checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)

    # This is the URL to which the customer will be redirected after they are
    # done managing their billing with the portal.
    return_url = "http://localhost:8000/"

    portalSession = stripe.billing_portal.Session.create(
        customer=checkout_session.customer,
        return_url=return_url,
    )
    # portal_obj=PortalSession.objects.create(user=request.user,portal_session_id=portalSession.id)
    portal_obj = PortalSession.objects.filter(user=request.user).exists()
    if not portal_obj:
      portal=PortalSession.objects.create(user=request.user,portal_session_id=portalSession.id)
      portal.save()

    return redirect(portalSession.url, code=303)
  # else:
  #   subscription_obj = Subscription.objects.get(user=request.user)
  #   checkout_session_id = subscription_obj.checkouts_session_id
  #   checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
  #   return_url = "http://localhost:8000/plans/"
    
  #   portalSession = stripe.billing_portal.Session.retrieve(customer=checkout_session.customer, return_url=return_url,)
  #   return redirect(portalSession.url, code=303)

def cancel(request):
  sub_obj = Subscription.objects.filter(user=request.user).first()
  # portal_obj = PortalSession.objects.filter(user=request.user).first()
  # if portal_obj:
  #   portal_obj.delete()
  if sub_obj:
    sub_obj.delete()
    return render(request, "subscriptions/cancel.html")
  else:
    return "something went wrong! can't complete the request contact us if you need help"

def success(request):
  return render(request, "subscriptions/success.html")


# contex subscription for all templates

# @login_required
def subscription_status(request):
  if request.user.is_authenticated:
    subscription_obj = Subscription.objects.filter(user=request.user).first()
    if subscription_obj:
      checkout_session_id = subscription_obj.checkouts_session_id
      checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
      subscription_id = checkout_session.subscription
      subscription_obj = stripe.Subscription.retrieve(subscription_id)
      # start_date = subscription_obj.current_period_start
      # end_date = subscription_obj.current_period_end
      sub_status = subscription_obj.status
    else:
      sub_status = False
  else:
    # subscription_obj = Subscription.objects.filter(user=None).first()
    sub_status = False
  return {'has_premium_subscription': sub_status}


