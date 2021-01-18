from django import views
from django.urls import path

from core.tests import banner_create
from core.views.banners_views import BannerView, BannerDetailView
from core.views.setting_views import update_setting
from core.views.views import AddCategory, ProductView, ProductUpdate, ProductCreate, ProductDelete, categories, index, \
    EditCategory, DeleteCategory, ProductDetailView, AddProductView, EditProductView, products_admin

app_name = 'core'
urlpatterns = [


    path('admin/', index, name='index'),


        ########## categories  #########
    path('admin/category/', categories, name='categories'),
    path('admin/category/edit/<int:id>/<slug:slug>', EditCategory.as_view(), name='EditCategory'),
    path('admin/category/add/', AddCategory.as_view(), name='AddCategory'),
    path('admin/category/delete/<int:id>/<slug:slug>/', DeleteCategory.as_view(), name='delete_category'),


       ########## Products   #########
    #path('admin/products/', views.products_admin, name='products_admin'),
    path('admin/product/', products_admin, name='products_admin'),
    path('admin/product/<int:pk>/', ProductDetailView.as_view(), name='ProductDetail'),
    #path('admin/catalog/edit/<int:pk>/<slug:slug>/',EditProductView(), name='ProductUpdate'),
    path('admin/product/edit/', EditProductView, name='ProductUpdate'),
    #path('admin/catalog/create/', ProductCreate.as_view(), name='ProductCreate'),
    path('admin/product/create/', AddProductView, name='ProductCreate'),
    #path('admin/catalog/create/', addProductView, name='addProductView'),
    path('admin/product/delete/<int:id>/<slug:slug>/', ProductDelete.as_view(), name='ProductDelete'),

    ########## options  #########
    path('admin/options/', categories, name='options'),
    path('admin/options/edit/<int:id>/<slug:slug>', EditCategory.as_view(), name='EditoOtions'),
    path('admin/options/add/', AddCategory.as_view(), name='AddOptions'),
    path('admin/options/delete/<int:id>/<slug:slug>/', DeleteCategory.as_view(), name='delete_options'),

    ########## Manufacturer   #########
    # path('admin/products/', views.products_admin, name='products_admin'),
    #path('admin/manufacturer/', views.AddManufacturer, name='manufacturer'),
    #path('admin/catalog/<int:pk>/', views.ProductDetailView.as_view(), name='ProductDetail'),
    #path('admin/catalog/edit/<int:pk>/<slug:slug>/', ProductUpdate.as_view(), name='ProductUpdate'),
    # path('admin/catalog/create/', ProductCreate.as_view(), name='ProductCreate'),
    #path('admin/catalog/create/', addProductView, name='addProductView'),
    #path('admin/catalog/delete/<int:id>/<slug:slug>/', ProductDelete.as_view(), name='ProductDelete'),


    #path('admin/catalog/', ProductView.as_view(), name='ProductView'),
    #path('admin/catalog/create/', ProductCreateView.as_view(), name='ProductCreateView'),
    #path('admin/catalog/<int:pk>/', ProductDetailView.as_view(), name='ProductDetailView'),


      ########## Manufacturer   #########
    path('admin/setting/', update_setting, name='update_setting'),

    ########## Banners   #########
    path('admin/banner', BannerView.as_view(), name='BannerView'),
	path('admin/banner/<int:pk>/', BannerDetailView.as_view(), name='BannerDetailView'),
    path('admin/banner/create/',banner_create, name='add_banner'),


]