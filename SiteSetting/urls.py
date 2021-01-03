from django.urls import path

from . import views
from .views import setting,  update_setting

app_name = 'SiteSetting'
urlpatterns = [
    #path('admin/setting/', setting, name='setting'),
    path('admin/setting/', update_setting, name='update_setting'),



        ########## Setting  #########
   # path('admin/setting/<int:id>/<slug:slug>/', views.setting, name='categories'),
   # path('admin/setting/<int:id>/', EditSetting.as_view(), name='EditSetting'),
    #path('admin/setting/', AddSetting.as_view(), name='AddSetting'),



]