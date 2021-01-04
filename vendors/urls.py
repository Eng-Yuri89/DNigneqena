from django import views
from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import path


from vendors.views import store_list, store_page, edit_store, store_delete, AddStore

app_name = 'vendors'


urlpatterns = [
    #path('v/login/',SellerLoginView.as_view(),name='seller_login'),
    #path('v/register/',SellerRegisterView.as_view(),name='seller_register'),
    path('logout/',LogoutView.as_view(),name='seller_logout'),



    path('admin/s',store_list,name='store_list'),
    path('admin/s/create',AddStore.as_view(),name='AddStore'),
    path('admin/s/<int:id>',store_page,name='store_page'),
    path('admin/s/edit/', edit_store, name='edit_store'),
    #path('admin/create-profile',AddProfile.as_view(),name='create_profile'),

    path('admin/s/<int:id>', store_delete, name='store_delete'),
    #path('users/', UsersView.as_view(), name='UserList'),
    #path('create-user/', UserAdminCreationForm, name='CreateUser'),






]