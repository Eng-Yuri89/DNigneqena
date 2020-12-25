from django.urls import path

from . import api
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.index, name='admin/index'),
    # path('category/', views.category_list, name='category_list'),

    path('category/', views.category_list, name='category_list'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    # API
    path('api/category', api.category_list_api, name='category_list_api'),
    path('api/category/<int:id>', api.category_details_api, name='category_details_api'),
    path('admin/api/category', api.category_list_api, name='category_list_api'),

    # class based views

    path('api/v2/category/', api.CategoryListAPi.as_view(), name='CategoryListAPi'),
    path('api/v2/category/<int:id>', api.CategoryApi.as_view(), name='CategoryAPi'),
    path('api/v2/category/product/', api.ProductListApi.as_view(), name='ProductListAPi'),
    path('api/v2/category/product/<int:id>', api.ProductApi.as_view(), name='ProductAPi'),

]
