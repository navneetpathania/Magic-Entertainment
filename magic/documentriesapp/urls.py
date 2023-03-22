from django.urls import path,include
from . import views 


urlpatterns = [
    path('', views.documentary_list, name='documentries'),
    path('download/<int:pk>', views.documentary_download, name='documentary_download'),
    path('play_documentary/<int:pk>', views.play_documentary, name='play_documentary'),
    path('documentary_history', views.historyView, name='documentary_history'),
    path('mark_fav/', views.mark_as_favorite, name='mark_documentary_as_favorite'),
    path('feedback/', views.like_dislike, name='documentary_like_dislike'),
]