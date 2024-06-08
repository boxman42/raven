from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="Ravnn_Home"),
    path("about/", views.about, name="About")
]