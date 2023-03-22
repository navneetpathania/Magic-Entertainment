from django.urls import path,include
from . import views 


urlpatterns = [
   
    path('', views.songs_view, name='songs'),
    path('play_song/<int:pk>/', views.play_song, name='play_song'),
    path('download/<int:pk>/', views.song_download_view, name='song_download'),
    path('history/',views.historyView ,name='song_history'),
    path('mark_fav/', views.mark_as_favorite, name='mark_song_as_favorite'),
    path('feedback/',views.like_dislike ,name='song_like_dislike')
]