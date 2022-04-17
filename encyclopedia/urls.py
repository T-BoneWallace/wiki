from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("random", views.random_entry, name="random"),
    path("edit", views.edit, name="edit"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("update", views.update, name="update"),
    path("test", views.test, name="test")
]
