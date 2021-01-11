from django import views
from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import path


from vendors.views import store_list,  edit_store, store_delete, create_success, \
     become_seller, vendor_dashboard, admin_dashboard

app_name = 'vendors'


urlpatterns = [
    #path('v/login/',SellerLoginView.as_view(),name='seller_login'),
    #path('v/register/',SellerRegisterView.as_view(),name='seller_register'),

    ###############Adminn Seller Url##############
    path('admin/s',store_list,name='store_list'),
    path('admin/s/<int:id>',admin_dashboard,name='store_page'),
    path('admin/s/edit/', edit_store, name='edit_store'),
    path('admin/s/<int:id>', store_delete, name='store_delete'),



    ###############Front Seller Url##############
    path('become_seller/<int:id>',become_seller,name='become_seller'),
    path('create_success/',create_success,name='create_success'),
    path('s/',vendor_dashboard,name='vendor_dashboard'),







]