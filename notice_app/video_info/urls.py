from django.urls import path
from . import views

app_name = "video_info"
urlpatterns = [
    path("", views.index, name="index"),
    path("main/", views.info_main, name="info_main"),
    path("send/", views.info_send, name="info_send"),
]
