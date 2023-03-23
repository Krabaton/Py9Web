from django.contrib import admin
from django.urls import path
from . import views

app_name = "app_instagram"

urlpatterns = [
    path("", views.main, name='root'),
    path("upload/", views.upload, name='upload'),
    path("pictures/", views.pictures, name='pictures'),
    path("pictures/edit/<int:pic_id>", views.edit, name='edit'),
    path("pictures/remove/<int:pic_id>", views.remove, name='remove'),
]
