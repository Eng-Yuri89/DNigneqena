"""DNigne URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from catalog import views ,api
from catalog.serializers import CategorySerializer
from home import views
from users import views as UserViews

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='home'),
    path('home/', include('home.urls')),

    path('', include('catalog.urls'),name='catalog'),

    #path('admin/', include(admin.site.urls),'admin'),

    # Catelog Url




    # USER URL
    path('users/<int:id>', views.user_list, name='user_list'),

    # LOGIN URL
    path('login/', UserViews.login_form, name='login'),
    path('logout/', UserViews.logout_func, name='logout'),
    path('signup/', UserViews.signup_form, name='signup'),



    #ADMIN URL
    #path('admin/category/', views.category_admin, name='category_admin'),
    path('admin/category/', views.category_admin, name='category_admin'),


    # jet admin dshboard
    #path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    #path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS


    #API URL
    path('api-auth/', include('rest_framework.urls')),




]

# ... the rest of your URLconf goes here ...
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
