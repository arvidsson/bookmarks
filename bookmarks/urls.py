from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("add/", views.add, name="add"),
    path("delete/<int:bookmark_id>/", views.delete, name="delete"),
    path("edit/<int:bookmark_id>/", views.edit, name="edit"),
    path("search/", views.search, name="search"),
    path("tag/<str:tag_name>/", views.tag, name="tag"),
]