from django.urls import path

from . import views


urlpatterns = [
    path("upload/clearfile", views.clearFile, name="clearFile"),
]