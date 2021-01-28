from django.urls import path, include

from . import views
from .search import SearchView
from .views import ProductDetailView, autocomplete, ProductsView

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.index, name='index'),
    path('search/autocomplete', autocomplete, name='autocomplete'),
    #path('search/', SearchView(), name='search'),

    #path('search_auto/', views.search_auto, name='search_auto'),

    ############ Category Product ##############
    path('products/', ProductsView.as_view(), name='ProductsView'),


    ############ Product ##############
    path('product/<int:pk>/', ProductDetailView.as_view(), name='ProductDetail'),
    #path('search/<int:pk>/', ProductDetailView.as_view(), name='ProductDetail'),

]