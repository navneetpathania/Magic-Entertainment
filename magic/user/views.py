from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .form import UserRegisterForm,userUpdateForm,profileUpdateForm
from django.contrib import messages
from .models import CreateProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from subscriptions.models import Subscription
from django.conf import settings
import datetime
import stripe
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data.get('username')
			messages.success(request,f'Account is created for {username}')
			form.save()
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request,'user/register.html',{'form':form})

@login_required
def profile(request):
	if request.method == 'POST':
		u_form = userUpdateForm(request.POST,instance=request.user)
		i_form = profileUpdateForm(request.POST,request.FILES,instance=request.user.createprofile)
		if u_form.is_valid() and i_form.is_valid():
			u_form.save()
			i_form.save()
			messages.success(request,'Your account is updated successfully!')
			return redirect('profile')
		else:
			context = {
				'u_form':u_form,
				'i_form':i_form
				}
			return render(request,'user/profile.html',context)

	else:
		u_form = userUpdateForm(instance=request.user)
		i_form = profileUpdateForm(instance=request.user.createprofile)
		context = {
		'u_form':u_form,
		'i_form':i_form
		}
		# subscription = Subscription.objects.filter(user=request.user).exists()
		# if subscription:
		# 	context['subscription'] = "Active"
		# else:
		# 	context['subscription'] = "Not active"

		# sta = Subscription.objects.filter(User__id=request.user.id)

		subscription = Subscription.objects.filter(user=request.user).exists()
		if subscription:
			subscription_obj = Subscription.objects.filter(user=request.user).first()
			checkout_session_id = subscription_obj.checkouts_session_id
			checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
			subscription_id = checkout_session.subscription
			# print(checkout_session)

			subscription_obj = stripe.Subscription.retrieve(subscription_id)
			start_date = subscription_obj.current_period_start
			end_date = subscription_obj.current_period_end
			status = subscription_obj.status
			context['status'] = status
			
			start_date_datetime = datetime.datetime.fromtimestamp(start_date)
			end_date_datetime = datetime.datetime.fromtimestamp(end_date)
			context['start_date'] = start_date_datetime
			context['end_date'] = end_date_datetime

		return render(request,'user/profile.html',context)

