from django import views
from django.urls import path

from core.views.setting_views import update_setting
from core.views.views import AddCategory, ProductView, ProductUpdate, ProductCreate, ProductDelete, categories, index, \
    EditCategory, DeleteCategory, ProductDetailView, AddProductView, EditProductView

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
    path('admin/product/', ProductView.as_view(), name='product'),
    path('admin/product/<int:pk>/', ProductDetailView.as_view(), name='ProductDetail'),
    #path('admin/product/edit/<int:pk>/<slug:slug>/',EditProductView(), name='ProductUpdate'),
    path('admin/product/edit/<int:id>/<slug:slug>/', ProductUpdate.as_view(), name='ProductUpdate'),
    #path('admin/product/create/', ProductCreate.as_view(), name='ProductCreate'),
    path('admin/product/create/', AddProductView, name='ProductCreate'),
    #path('admin/product/create/', addProductView, name='addProductView'),
    path('admin/product/delete/<int:id>/<slug:slug>/', ProductDelete.as_view(), name='ProductDelete'),

    ########## options  #########
    path('admin/options/', categories, name='options'),
    path('admin/options/edit/<int:id>/<slug:slug>', EditCategory.as_view(), name='EditoOtions'),
    path('admin/options/add/', AddCategory.as_view(), name='AddOptions'),
    path('admin/options/delete/<int:id>/<slug:slug>/', DeleteCategory.as_view(), name='delete_options'),

    ########## Manufacturer   #########
    # path('admin/products/', views.products_admin, name='products_admin'),
    #path('admin/manufacturer/', views.AddManufacturer, name='manufacturer'),
    #path('admin/product/<int:pk>/', views.ProductDetailView.as_view(), name='ProductDetail'),
    #path('admin/product/edit/<int:pk>/<slug:slug>/', ProductUpdate.as_view(), name='ProductUpdate'),
    # path('admin/product/create/', ProductCreate.as_view(), name='ProductCreate'),
    #path('admin/product/create/', addProductView, name='addProductView'),
    #path('admin/product/delete/<int:id>/<slug:slug>/', ProductDelete.as_view(), name='ProductDelete'),


    #path('admin/product/', ProductView.as_view(), name='ProductView'),
    #path('admin/product/create/', ProductCreateView.as_view(), name='ProductCreateView'),
    #path('admin/product/<int:pk>/', ProductDetailView.as_view(), name='ProductDetailView'),


      ########## Manufacturer   #########
    path('admin/setting/', update_setting, name='update_setting'),


]