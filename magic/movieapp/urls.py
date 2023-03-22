from django.urls import path,include
from . import views 


urlpatterns = [
    path('', views.movie_list, name='movies'),
    path('download/<int:pk>', views.movie_download, name='movie_download'),
    path('play_movie/<int:pk>', views.play_movie, name='play_movie'),
    path('history/', views.historyView, name='history'),
    path('mark_fav/', views.mark_as_favorite, name='mark_as_favorite'),
    path('feedback/', views.like_dislike, name='like_dislike'),
]