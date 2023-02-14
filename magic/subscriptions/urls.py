
from django.urls import path,include
from . import views 


urlpatterns = [
    path('', views.plans, name='plans'),
    path('subscribe/<int:plan_id>/', views.subscribe, name='subscribe'),
    path('cancel/<int:subscription_id>/', views.cancel, name='cancel'),
    path('charge/', views.charge,name='charge')
]
