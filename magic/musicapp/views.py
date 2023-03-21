from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from .models import Song, Genre, History
from subscriptions.models import Subscription
from django.core.paginator import Paginator
from django.db.models import Count, Case, When, Q
from collections import Counter
# Create your views here.

def songs_view(request):
    songs = Song.objects.all()
    popular_songs = Song.objects.all().order_by('-total_likes')[:10]
    latest_songs = Song.objects.order_by('-created_at')
    genres = Genre.objects.annotate(num_songs=Count('songsgenre')).filter(num_songs__gt=0)
    history_obj = History.objects.filter(user=request.user)
    obj = reversed(history_obj)
    most_common_genres = songs_suggestion(request)
    recomendations = Song.objects.filter(Q(genre__name__in=most_common_genres)).exclude(songhistory__user=request.user)[:10]
    return render(request, 'musicapp/songs.html', {'songs': songs,'popular_songs':popular_songs, 'latest_songs':latest_songs, 'genres':genres,
    'recent_played':obj, 'recomendations':recomendations})

def songs_suggestion(request):
    user = request.user
    history = user.usersonghistory.all()
    genres =  [h.song.genre for h in history]
    genre_counts = Counter(genre.name for genre in genres)
    most_common_genres = [genre_count[0] for genre_count in genre_counts.most_common(2)]
    return most_common_genres

def play_song(request, pk):
    song = get_object_or_404(Song, pk=pk)
    next_song = Song.objects.filter(id__gt=song.id).order_by('id').first()
    prev_song = Song.objects.filter(id__lt=song.id).order_by('-id').first()
    return render(request, 'musicapp/song.html',{"song":song,'next_song':next_song ,'prev_song':prev_song})
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