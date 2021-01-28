from django.conf.urls import url
from django.urls import path

from sales.views import views ,order , cart
from sales.views.views import shopcart

app_name = 'sales'

urlpatterns = [
    path('cart/', views.index, name='index'),
    path('cart/addtoshopcart/<int:id>', views.addtoshopcart, name='addtoshopcart'),
    path('cart/deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),

    path('cart/orderproduct/', views.orderproduct, name='orderproduct'),
    path('shopcart/', shopcart, name='shopcart'),
]