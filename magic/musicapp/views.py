from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from .models import Song, Genre
from subscriptions.models import Subscription
from django.core.paginator import Paginator
from django.db.models import Count
# Create your views here.

def songs_view(request):
    # subscribed = Subscription.objects.get(user=request.user)
    # if subscribed:
    #     songs = Song.objects.all()
    # else:
    #     songs = Song.objects.filter(subscription_only=False)
    songs = Song.objects.all()
    popular_songs = Song.objects.all().order_by('-total_likes')
    latest_songs = Song.objects.order_by('-created_at')
    rap = Genre.objects.get(name='rap')
    romatic = Genre.objects.get(name='Romatic songs')
    rap_songs = Song.objects.filter(genre=rap)
    romatic_songs = Song.objects.filter(genre=romatic)
    # paginator = Paginator(song, 4)
    # page = request.GET.get('page')
    # songs = paginator.get_page(page)
    # songrange = range(0, len(song), 4)
    
    return render(request, 'musicapp/songs.html', {'songs': songs,'popular_songs':popular_songs, 'latest_songs':latest_songs, 'rap_songs':rap_songs, "romatic_songs":romatic_songs})

def play_song(request, pk):
    song = get_object_or_404(Song, pk=pk)
    return render(request, 'musicapp/song.html',{"song":song})
def song_download_view(request, pk):
    song = get_object_or_404(Song, pk=pk)
    file = song.audio_file
    response = FileResponse(file)
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    return response
