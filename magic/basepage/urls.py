
from django.urls import path,include
from . import views 


urlpatterns = [
    path('',views.landingView,name='landingpage'),
    path('home/',views.homeView,name='home'),
    path('about/',views.aboutView,name='about'),
    path('contact/',views.contactView, name='contact_us')
]
