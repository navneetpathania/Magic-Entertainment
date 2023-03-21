from django.contrib import admin
from django.urls import path,include
from user import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from basepage.views import searchView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('basepage.urls')),
    path('search/',searchView, name='search'),
    path("music/",include('musicapp.urls')),
    path("movies/",include('movieapp.urls')),
    path("museums/",include('virtualtour.urls')),
    path("documentary/",include('documentriesapp.urls')),
    path('plans/',include('subscriptions.urls')),
    path('login/',auth_views.LoginView.as_view(template_name='user/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='user/logout.html'),name='logout'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='user/password_reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),name='password_reset_complete'),
    path('register/',user_views.register,name='user-register'),
    path('profile/',user_views.profile,name='profile'),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)