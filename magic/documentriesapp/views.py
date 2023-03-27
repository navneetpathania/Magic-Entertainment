from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from .models import Documentary, Category, History
from django.db.models import Count,Q
from collections import Counter
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from subscriptions.models import Subscription
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def documentary_list(request):
    documentaries = Documentary.objects.all()
    popular_documentaries = Documentary.objects.all().order_by('-total_likes')
    latest_documentaries = Documentary.objects.order_by('-created_at')
    categorys = Category.objects.annotate(num_documentary=Count('documentary')).filter(num_documentary__gt=0)
    history_obj = History.objects.filter(user=request.user)
    obj = reversed(history_obj)
    most_common_category = documentary_suggestion(request)
    liked = Documentary.objects.filter(liked_by=request.user)
    recomendations = Documentary.objects.filter(Q(category__name__in=most_common_category)).exclude(documentaryhistory__user=request.user)[:10]

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
        # context['status'] = status
    else:
        status = False

    return render(request, 'documentariesapp/documentary_list.html', {'documentaries': documentaries, 'popular_documentaries':popular_documentaries, 
    'latest_documentaries':latest_documentaries, 'categorys':categorys, 'recent_played':obj, 
    'recomendations':recomendations,'liked':liked, 'status':status})

def documentary_suggestion(request):
    user = request.user
    history = user.userdocumentaryhistory.all()
    category =  [h.documentary.category for h in history]
    genre_counts = Counter(genre.name for genre in category)
    most_common_category = [genre_count[0] for genre_count in genre_counts.most_common(2)]
    return most_common_category

def documentary_download(request, pk):
    documentary = Documentary.objects.get(pk=pk)
    response = FileResponse(open(documentary.documentray_file.path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(documentary.documentray_file.name)
    return response

def play_documentary(request, pk):
    documentary = get_object_or_404(Documentary, pk=pk)
    user = request.user
    favs = user.userfavdocumentray.all()
    if documentary in favs:
        # movie exists in favorites
        is_favorite = True
    else:
        # movie doesn't exist in favorites
        is_favorite = False
    return render(request, 'documentariesapp/documentary.html',{"documentary":documentary, "is_favorite":is_favorite})

def historyView(request):
    if request.method == "POST":
        user = request.user
        documentary_id = request.POST['documentary_id']
        documentary = Documentary.objects.get(id=documentary_id)
        history, created = History.objects.get_or_create(user=user, documentary=documentary)
        if created:
            history.save()
            return redirect(f"/documentary/play_documentary/{documentary_id}")
        else:
            # If an object with the same documentary_id already exists, do nothing
            return redirect(f"/documentary/play_documentary/{documentary_id}")
    history = History.objects.filter(user=request.user)
    documentaries = []
    for i in history:
        documentaries.append(i.documentary)
    # documentaries = documentary.objects.filter(id__in=documentaries)
    return render(request,'documentaryapp/history.html', {"history":documentaries})

@login_required
def mark_as_favorite(request):
    documentary_id = request.POST['documentary_id']
    documentary = get_object_or_404(Documentary, id=documentary_id)
    # favorite, created = Favorite.objects.get_or_create(documentary=documentary, user=request.user)
    is_fav = Documentary.objects.filter(fav=request.user, id=documentary_id).exists()
    if is_fav:
        documentary.fav.remove(request.user)
        documentary.save()
        
        messages.warning(request, 'Documentary removed from favorites')
    else:
        
        documentary.fav.add(request.user)
        documentary.save()
        
        messages.success(request, 'Documentary added to favorites.')

    return redirect(f'/documentary/play_documentary/{documentary_id}')
from django.http import JsonResponse

@login_required
def like_dislike(request):
    documentary_id = request.GET.get('documentary_id')    
    documentary = Documentary.objects.get(id=documentary_id)
    user = request.user
    liked = Documentary.objects.filter(liked_by=request.user, id=documentary_id).exists()
    if not liked:
        # documentary.total_likes +=1
        documentary.liked_by.add(request.user)
        documentary.save()
        documentary = Documentary.objects.get(id=documentary_id)
        
        total_likes = documentary.liked_by.all().count()
        documentary.total_likes = total_likes
        documentary.save()

        response = {
        "total_likes": total_likes, "liked":True
        }
        return JsonResponse(response)
    else:
        # documentary.total_likes -=1
        documentary.liked_by.remove(request.user)
        documentary.save()
        documentary = Documentary.objects.get(id=documentary_id)
        total_likes = documentary.liked_by.all().count()
        documentary.total_likes = total_likes
        documentary.save()
        response = {
        "total_likes": total_likes, "liked":False
        }
    
        return JsonResponse(response)