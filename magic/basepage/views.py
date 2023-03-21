from django.shortcuts import render, get_object_or_404
from subscriptions.models import Subscription
from musicapp.models import Song
from movieapp.models import Movie
from documentriesapp.models import Documentary
from django.contrib.auth.models import User

# Create your views here.
def homeView(request):
    try:
        sub_obj = Subscription.objects.get(user=request.user)
        sub_status = sub_obj.active
    except:
        sub_status = False
    print(request.user)
    return render(request, "basepage/home.html",{'sub_status':sub_status})

def searchView(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        result1 = Song.objects.filter(title__icontains=search_query)
        result2 = Movie.objects.filter(title__icontains=search_query)
        result3 = Documentary.objects.filter(title__icontains=search_query)
        results = list(result1)+list(result2)+list(result3)
        
        return render(request, 'basepage/search_results.html', {'music': result1,'movies':result2,
        'documentaries':result3, 'search_query':search_query, 'results':results})




