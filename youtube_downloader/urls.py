from django.urls import path
from . import views 
urlpatterns = [
    path('',views.home, name='home') , 
    path('video/',views.video_info, name='video_info') , 
    path('<str:id>/<str:format>/<str:vtype>/',views.download, name='download') , 
    path('<str:id>/<str:format>/<str:vtype>/',views.download, name='download') ,
]