from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.view_entry, name="view_entry"),
    path("create_entry", views.create_entry, name="create_entry"),
    path("edit_entry/<str:entry>", views.edit_entry, name="edit_entry"),
    path("random_entry/<str:entry>", views.random_entry, name="random_entry"),
    path("random_entry", views.random_entry, name="random_entry"),
]
