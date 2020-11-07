from django.urls import path
from . import views 
urlpatterns = [
    path('',views.home, name='home') , 
    path('video/',views.video_info, name='video_info') , 
    path('video/download/<str:id>/<str:format>/',views.download, name='download') , 
]