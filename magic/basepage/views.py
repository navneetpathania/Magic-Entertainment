from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from subscriptions.models import Subscription
from musicapp.models import Song
from movieapp.models import Movie
from documentriesapp.models import Documentary
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

# Create your views here.
@login_required
def homeView(request):
    return render(request, "basepage/home.html")


def searchView(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        result1 = Song.objects.filter(title__icontains=search_query)
        result2 = Movie.objects.filter(title__icontains=search_query)
        result3 = Documentary.objects.filter(title__icontains=search_query)
        results = list(result1)+list(result2)+list(result3)
        subscription = Subscription.objects.filter(user=request.user).exists()
        liked = Movie.objects.filter(liked_by=request.user)
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
            # context['status'] = status
        else:
            status = False
        
        return render(request, 'basepage/search_results.html', {'music': result1,'movies':result2,
        'documentaries':result3, 'search_query':search_query,'liked':liked, 'results':results,'status':status})


def contactView(request):
    if request.method == "POST":
        name = request.POST['name']
        user_email = request.POST['email']
        subject= request.POST['subject']
        message = request.POST['message']

        email = EmailMessage(
            subject, # Email subject
            message, # Email message
            'navneetpathania210@gmail.com', # Email sender
            [user_email], # Email receivers
            
        )
        email.send()
        return render(request, 'basepage/contact-success.html')

        
    
def aboutView(request):
    return render(request, 'basepage/about.html')

def landingView(request):
    return render(request, 'basepage/landingpage.html')