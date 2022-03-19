from django.urls import path

from . import views


urlpatterns = [
    path("", views.UploadView.as_view(), name="upload"),
    path("<int:pk>", views.UploadDetailView.as_view(), name="detail"),
    path("<int:pk>/download", views.DownloadView.as_view(), name="download"),
    path("<int:pk>/delete", views.DeleteView.as_view(), name="delete"),
    path("list", views.ListView, name="list"),
]