from django import views
from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views.customer import customer_logout, CustomerRegister, CustomerLoginView, RegistrationView, EmailValidationView, \
    VerificationView
from .views.views import UserLoginView, RegisterView, update_profile, guest_user_view, user_list, user_profile, \
    user_delete

app_name = 'accounts'


urlpatterns = [
    path('login/',UserLoginView.as_view(),name='user_login'),
    path('register/',RegisterView.as_view(),name='user_register'),
    path('logout/',LogoutView.as_view(),name='user_logout'),



    path('admin/users',user_list,name='user_list'),
    path('admin/profile/<int:id>',user_profile,name='user_profile'),
    path('admin/uprofile/', update_profile, name='update_profile'),
    #path('admin/create-profile',AddProfile.as_view(),name='create_profile'),
    path('guest-user/',guest_user_view,name='guest_user_register'),
    path('admin/dprofile/<int:id>', user_delete, name='user_delete'),
    #path('users/', UsersView.as_view(), name='UserList'),
    #path('create-user/', UserAdminCreationForm, name='CreateUser'),


    ##########Customer################

    path('home/login/',CustomerLoginView.as_view(),name='customer_login'),
    path('home/register/',CustomerRegister.as_view(),name='customer_register'),
    path('home/logout/',customer_logout,name='customer_logout'),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()),
         name='validate_email'),
    path('activate/<uidb64>/<token>',
         VerificationView.as_view(), name='activate'),
    #path('user/profile',profile,name='customer_profile'),
    #path('user/uprofile/', update_profile, name='customer_update_profile'),
    #path('admin/create-profile',AddProfile.as_view(),name='create_profile'),
    #path('guest-user/',guest_user_view,name='guest_user_register'),
    #path('users/', UsersView.as_view(), name='UserList'),
    #path('create-user/', UserAdminCreationForm, name='CreateUser'),




]