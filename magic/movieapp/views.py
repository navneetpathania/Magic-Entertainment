from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from .models import Movie, Genre, History
from django.db.models import Count,Q
from collections import Counter
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from subscriptions.models import Subscription
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
@login_required
def movie_list(request):
    movies = Movie.objects.all()
    popular_movies = Movie.objects.all().order_by('-total_likes')
    latest_movies = Movie.objects.order_by('-created_at')
    genres = Genre.objects.annotate(num_movies=Count('movies')).filter(num_movies__gt=0)
    history_obj = History.objects.filter(user=request.user)
    obj = reversed(history_obj)
    most_common_genres = movie_suggestion(request)
    recomendations = Movie.objects.filter(Q(genres__name__in=most_common_genres)).exclude(moviehistory__user=request.user)[:10]
    liked = Movie.objects.filter(liked_by=request.user)

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
    return render(request, 'movieapp/movie_list.html', {'movies': movies, 'popular_movies':popular_movies, 
    'latest_movies':latest_movies, 'genres':genres,'recent_played':obj,
    'liked':liked,'recomendations':recomendations, 'status':status})

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
    user = request.user
    favs = user.userfavmovie.all()
    if movie in favs:
        # movie exists in favorites
        is_favorite = True
    else:
        # movie doesn't exist in favorites
        is_favorite = False
        
    return render(request, 'movieapp/movie.html',{"movie":movie, "is_favorite":is_favorite})

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
def mark_as_favorite(request):
    movie_id = request.POST['movie_id']
    movie = get_object_or_404(Movie, id=movie_id)
    # favorite, created = Favorite.objects.get_or_create(movie=movie, user=request.user)
    is_fav = Movie.objects.filter(fav=request.user, id=movie_id).exists()
    if is_fav:
        movie.fav.remove(request.user)
        movie.save()
        
        messages.warning(request, 'Movie removed from favorites')
    else:
        # movie.total_likes += 1
        # movie.liked_by.add(request.user)
        movie.fav.add(request.user)
        movie.save()
        
        messages.success(request, 'Movie added to favorites.')
    # return render(request, 'movieapp/movie.html', {'movie':movie,'favorite':fav})
    return redirect(f'/movies/play_movie/{movie_id}')
from django.http import JsonResponse

@login_required
def like_dislike(request):
    movie_id = request.GET.get('movie_id')    
    movie = Movie.objects.get(id=movie_id)
    user = request.user
    liked = Movie.objects.filter(liked_by=request.user, id=movie_id).exists()
    if not liked:
        # movie.total_likes +=1
        movie.liked_by.add(request.user)
        movie.save()
        movie = Movie.objects.get(id=movie_id)
        
        total_likes = movie.liked_by.all().count()
        movie.total_likes = total_likes
        movie.save()

        response = {
        "total_likes": total_likes, "liked":True
        }
        return JsonResponse(response)
    else:
        # movie.total_likes -=1
        movie.liked_by.remove(request.user)
        movie.save()
        movie = Movie.objects.get(id=movie_id)
        total_likes = movie.liked_by.all().count()
        movie.total_likes = total_likes
        movie.save()
        response = {
        "total_likes": total_likes, "liked":False
        }
    
        return JsonResponse(response)