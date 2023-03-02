from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from .models import Song, Movie
from subscriptions.models import Subscription
import datetime
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

def songs_view(request):
    subscribed = Subscription.objects.get(user=request.user)
    if subscribed:
        songs = Song.objects.all()
    else:
        songs = Song.objects.filter(subscription_only=False)
    
    return render(request, 'basepage/songs.html', {'songs': songs})


def song_download_view(request, pk):
    song = get_object_or_404(Song, pk=pk)
    file = song.audio_file
    response = FileResponse(file)
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    return response

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'basepage/movie_list.html', {'movies': movies})

def movie_download(request, pk):
    movie = Movie.objects.get(pk=pk)
    response = FileResponse(open(movie.video_file.path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(movie.video_file.name)
    return response