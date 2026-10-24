from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("myapp/", include("myapp.urls")),
    # Send the site root to the board page.
    path("", RedirectView.as_view(pattern_name="board", permanent=False)),
]
