
from django.urls import path,include
from .views import * 


urlpatterns = [
    path('',checkout, name="plans"),
    path("create-checkout-session/", create_checkout_session, name="create-checkout-session"),
    path("create-portal-session/", create_portal_session, name="create-portal-session"), #add
    path("success/", success, name="success"),
    path('cancel/', cancel, name='cancel')
    # path('subscribe/<int:plan_id>/', views.subscribe, name='subscribe'),
    # path('cancel/<int:subscription_id>/', views.cancel, name='cancel'),
    # path('charge/', views.charge,name='charge'),
    # path('subscribe/', create_subscription, name='subscribe'),
    # path('update/', update_subscription, name='update_subscription'),
    # path('cancel/', cancel_subscription, name='cancel_subscription'),
    # path('detail/', subscription_detail, name='subscription_detail'),
]
