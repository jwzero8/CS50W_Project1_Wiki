from django.urls import path

from . import views

app_name = "wiki" # "wiki" is for the reference in html, wiki : <name in the path function>
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entryPage, name="entry"),
    path("search", views.search, name="search"),
    path("newPage", views.newPage, name="newPage"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("wiki/<str:title>/save", views.edit, name="save"),
    path("wiki/", views.randomPage, name="randomPage")
]
