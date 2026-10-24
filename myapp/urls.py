from django.urls import path

from . import views

urlpatterns = [
    path("", views.board_view, name="board"),          # post list + write form (stored XSS)
    path("search/", views.search_view, name="search"),  # search echo (reflected XSS)
]
