from django.urls import path,include
from . import views 


urlpatterns = [
    path('', views.museum_list, name='virtual_tour'),

]