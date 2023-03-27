
from django.urls import path,include
from . import views 


urlpatterns = [
    path('',views.homeView,name='home'),
    path('contact/',views.contactView, name='contact_us')
]
