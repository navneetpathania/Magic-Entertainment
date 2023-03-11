from django.urls import path,include
from . import views 


urlpatterns = [
    path('', views.movie_list, name='movies'),
    # path('download/<int:pk>', views.movie_download, name='movie_download'),
    # path('play_movie/<int:pk>', views.play_movie, name='play_movie'),
]