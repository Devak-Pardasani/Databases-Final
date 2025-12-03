from django.urls import path
from .views import movies_list

urlpatterns = [
    path("movies", movies_list),   # no trailing slash
]
