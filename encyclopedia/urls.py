from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.view_entry, name="view_entry"),
    path("create_entry", views.create_entry, name="create_entry"),
]
