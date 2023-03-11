from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from .models import Movie


def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movieapp/movie_list.html', {'movies': movies})

def movie_download(request, pk):
    movie = Movie.objects.get(pk=pk)
    response = FileResponse(open(movie.video_file.path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(movie.video_file.name)
    return response
def play_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'musicapp/song.html',{"movie":movie})