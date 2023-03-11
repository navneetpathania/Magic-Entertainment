from django.urls import path,include
from . import views 


urlpatterns = [
   
    path('', views.songs_view, name='songs'),
    path('play/<int:pk>/', views.play_song, name='play_song'),
    path('songs/<int:pk>/download/', views.song_download_view, name='song_download'),
]