from django.urls import path

from . import views
from .views import AddCategory, EditCategory, DeleteCategory, \
    ProductUpdate, ProductCreate, addProductView, ProductDelete, ProductView

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
        ########## categories  #########
    path('admin/category/', views.categories, name='categories'),
    path('admin/category/edit/<int:id>/<slug:slug>', EditCategory.as_view(), name='EditCategory'),
    path('admin/category/add/', AddCategory.as_view(), name='AddCategory'),
    path('admin/category/delete/<int:id>/<slug:slug>/', DeleteCategory.as_view(), name='delete_category'),


       ########## Products   #########
    #path('admin/products/', views.products_admin, name='products_admin'),
    path('admin/product/', ProductView.as_view(), name='product'),
    path('admin/product/<int:pk>/', views.ProductDetailView.as_view(), name='ProductDetail'),
    path('admin/product/edit/<int:pk>/<slug:slug>/',ProductUpdate.as_view(), name='ProductUpdate'),
    path('admin/product/create/', addProductView, name='ProductCreate'),
    #path('admin/product/create/', addProductView, name='addProductView'),
    path('admin/product/delete/<int:id>/<slug:slug>/', ProductDelete.as_view(), name='ProductDelete'),

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


]