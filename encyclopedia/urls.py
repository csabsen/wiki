from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("new/", views.new, name="new"),
    path("edit/<str:page>", views.edit, name="edit") 
    # path("random/", random.views, name="random")
]
