from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="hello-index"),
    path("about/", views.about, name="hello-about"),
]
