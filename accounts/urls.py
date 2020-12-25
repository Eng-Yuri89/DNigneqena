from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    UserLoginView,
    RegisterView,
    guest_user_view
)

app_name = 'accounts'


urlpatterns = [
    path('login/',UserLoginView.as_view(),name='user_login'),
    path('register/',RegisterView.as_view(),name='user_register'),
    path('logout/',LogoutView.as_view(),name='user_logout'),
    path('guest-user/',guest_user_view,name='guest_user_register'),




]