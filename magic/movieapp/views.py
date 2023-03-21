from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from .models import Movie, Genre, History
from django.db.models import Count,Q
from collections import Counter
from django.contrib.auth.decorators import login_required


def movie_list(request):
    movies = Movie.objects.all()
    popular_movies = Movie.objects.all().order_by('-total_likes')
    latest_movies = Movie.objects.order_by('-created_at')
    genres = Genre.objects.annotate(num_movies=Count('movies')).filter(num_movies__gt=0)
    history_obj = History.objects.filter(user=request.user)
    obj = reversed(history_obj)
    most_common_genres = movie_suggestion(request)
    recomendations = Movie.objects.filter(Q(genres__name__in=most_common_genres)).exclude(moviehistory__user=request.user)[:10]

    return render(request, 'movieapp/movie_list.html', {'movies': movies, 'popular_movies':popular_movies, 
    'latest_movies':latest_movies, 'genres':genres,'recent_played':obj,'recomendations':recomendations})

def movie_suggestion(request):
    user = request.user
    history = user.usermoviehistory.all()
    genres =  [h.movie.genres for h in history]
    genre_counts = Counter(genre.name for genre in genres)
    most_common_genres = [genre_count[0] for genre_count in genre_counts.most_common(2)]
    return most_common_genres
def movie_download(request, pk):
    movie = Movie.objects.get(pk=pk)
    response = FileResponse(open(movie.video_file.path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(movie.video_file.name)
    return response

def play_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'movieapp/movie.html',{"movie":movie})

def historyView(request):
    if request.method == "POST":
        user = request.user
        movie_id = request.POST['movie_id']
        movie = Movie.objects.get(id=movie_id)
        history, created = History.objects.get_or_create(user=user, movie=movie)
        if created:
            history.save()
            return redirect(f"/movies/play_movie/{movie_id}")
        else:
            # If an object with the same movie_id already exists, do nothing
            return redirect(f"/movies/play_movie/{movie_id}")
    history = History.objects.filter(user=request.user)
    movies = []
    for i in history:
        movies.append(i.movie)
    # movies = Movie.objects.filter(id__in=movies)
    return render(request,'movieapp/history.html', {"history":movies})


@login_required
def mark_as_favorite(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    # favorite, created = Favorite.objects.get_or_create(movie=movie, user=request.user)
    is_fav = movie.fav(user=request.user).exists()
    print(is_fav)
    # if not created:
    #     messages.warning(request, 'This movie is already in your favorites list.')
    # else:
    #     movie.total_likes += 1
    #     movie.liked_by.add(request.user)
    #     movie.save()
    #     messages.success(request, 'Movie added to favorites.')
    # return redirect('movie_detail', movie_id=movie_id)