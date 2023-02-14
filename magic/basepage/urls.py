
from django.urls import path,include
from . import views 


urlpatterns = [
   
    path('',views.homeView,name='home'),
    path('songs/', views.songs_view, name='songs'),
    path('songs/<int:pk>/download/', views.song_download_view, name='song_download'),
     path('movies/', views.movie_list, name='movies'),
    path('download/<int:pk>', views.movie_download, name='movie_download'),
]
