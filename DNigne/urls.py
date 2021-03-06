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
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from localization import views

urlpatterns = [
    path('selectlanguage', views.selectlanguage, name='selectlanguage'),
    #path('selectcurrency', views.selectcurrency, name='selectcurrency'),
    path('savelangcur', views.savelangcur, name='savelangcur'),
    path('i18n/', include('django.conf.urls.i18n')),
]
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('home.urls'),name='home'),
    path('', include('core.urls'),name='core'),
    path('', include('catalog.urls'),name='catalog'),
    path('',include('accounts.urls'),name='accounts'),
    path('', include('localization.urls'), name='localization'),
    path('',include('sales.urls'),name='sales'),
    path('', include('vendors.urls'), name='vendors'),
    path('search/', include('haystack.urls'), name='haystack'),
    # USER URL
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('imagefit/', include('imagefit.urls')),
    # LOGIN URL
    #API URL
    path('api-auth/', include('rest_framework.urls')),

 prefix_default_language=False,
)

# ... the rest of your URLconf goes here ...
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
