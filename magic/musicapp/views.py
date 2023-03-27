from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from .models import Song, Genre, History
from subscriptions.models import Subscription
from django.core.paginator import Paginator
from django.db.models import Count, Case, When, Q
from collections import Counter
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from subscriptions.models import Subscription
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

# Create your views here.
@login_required
def songs_view(request):
    songs = Song.objects.all()
    popular_songs = Song.objects.all().order_by('-total_likes')[:10]
    latest_songs = Song.objects.order_by('-created_at')
    genres = Genre.objects.annotate(num_songs=Count('songsgenre')).filter(num_songs__gt=0)
    history_obj = History.objects.filter(user=request.user)
    obj = reversed(history_obj)
    most_common_genres = songs_suggestion(request)
    liked = Song.objects.filter(liked_by=request.user)
    recomendations = Song.objects.filter(Q(genre__name__in=most_common_genres)).exclude(songhistory__user=request.user)[:10]
    # subscription check
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
    return render(request, 'musicapp/songs.html', {'songs': songs,'popular_songs':popular_songs, 'latest_songs':latest_songs, 'genres':genres,
    'recent_played':obj,'liked':liked ,'recomendations':recomendations,'status':status})

def songs_suggestion(request):
    user = request.user
    history = user.usersonghistory.all()
    genres =  [h.song.genre for h in history]
    genre_counts = Counter(genre.name for genre in genres)
    most_common_genres = [genre_count[0] for genre_count in genre_counts.most_common(2)]
    return most_common_genres

def play_song(request, pk):
    song = get_object_or_404(Song, pk=pk)
    user = request.user
    favs = user.userfavsong.all()
    if song in favs:
        # movie exists in favorites
        is_favorite = True
    else:
        # movie doesn't exist in favorites
        is_favorite = False
    next_song = Song.objects.filter(id__gt=song.id).order_by('id').first()
    prev_song = Song.objects.filter(id__lt=song.id).order_by('-id').first()
    return render(request, 'musicapp/song.html',{"song":song,'next_song':next_song ,'prev_song':prev_song,'is_favorite':is_favorite})
def song_download_view(request, pk):
    song = get_object_or_404(Song, pk=pk)
    file = song.audio_file
    response = FileResponse(file)
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    return response

def historyView(request):
    if request.method == "POST":
        user = request.user
        song_id = request.POST['song_id']
        song = Song.objects.get(id=song_id)
        history, created = History.objects.get_or_create(user=user, song=song)
        if created:
            history.save()
            return redirect(f"/music/play_song/{song_id}")
        else:
            # If an object with the same song_id already exists, do nothing
            return redirect(f"/music/play_song/{song_id}")
    history = History.objects.filter(user=request.user)
    songs = []
    for i in history:
        songs.append(i.song)
    # songs = Song.objects.filter(id__in=songs)
    return render(request,'musicapp/history.html', {"history":songs})

from django.http import JsonResponse

def mark_as_favorite(request):
    song_id = request.POST['song_id']
    song = get_object_or_404(Song, id=song_id)
    # favorite, created = Favorite.objects.get_or_create(Song=Song, user=request.user)
    is_fav = Song.objects.filter(fav=request.user, id=song_id).exists()
    if is_fav:
        song.fav.remove(request.user)
        song.save()
        
        messages.warning(request, 'Song removed from favorites')
    else:
        # Song.total_likes += 1
        # Song.liked_by.add(request.user)
        song.fav.add(request.user)
        song.save()
        
        messages.success(request, 'Song added to favorites.')
    # return render(request, 'Songapp/Song.html', {'Song':Song,'favorite':fav})
    return redirect(f'/music/play_song/{song_id}')

def like_dislike(request):
    song_id = request.GET.get('song_id')    
    song = Song.objects.get(id=song_id)
    user = request.user
    liked = Song.objects.filter(liked_by=request.user, id=song_id).exists()
    if not liked:
        
        song.liked_by.add(request.user)
        song.save()
        song = Song.objects.get(id=song_id)
        total_likes = song.liked_by.all().count()
        song.total_likes = total_likes
        song.save()
        response = {
        "total_likes": total_likes, "liked":True
        }
        return JsonResponse(response)
    else:
        
        song.liked_by.remove(request.user)
        song.save()
        song = Song.objects.get(id=song_id)
        total_likes = song.liked_by.all().count()
        song.total_likes = total_likes
        song.save()
        response = {
        "total_likes": total_likes, "liked":False
        }
    
        return JsonResponse(response)