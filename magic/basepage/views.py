from django.shortcuts import render, get_object_or_404
from subscriptions.models import Subscription



# Create your views here.
def homeView(request):
    try:
        sub_obj = Subscription.objects.get(user=request.user)
        sub_status = sub_obj.active
    except:
        sub_status = False
    print(request.user)
    return render(request, "basepage/home.html",{'sub_status':sub_status})
