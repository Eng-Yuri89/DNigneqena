from django.urls import path

from . import views
from .views import AddCategory, EditCategory, category_admin, DeleteCategory

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),

    path('admin/category/', views.category_admin, name='category_admin'),
    path('admin/category/add/', AddCategory.as_view(), name='AddCategory'),
    path('admin/category/<int:id>/<slug:slug>/edit', EditCategory.as_view(), name='EditCategory'),
    path('admin/category/delete/<int:id>/<slug:slug>/', DeleteCategory.as_view(), name='delete_category'),

    path('admin/products/', views.products_admin, name='products_admin'),
    path('admin/product/<int:id>/<slug:slug>/', views.product_admin, name='product_admin'),
    path('admin/product/add/', views.product_add, name='product_add'),
    path('admin/product/<int:id>/<slug:slug>/edit/', views.product_edit, name='product_edit'),

]