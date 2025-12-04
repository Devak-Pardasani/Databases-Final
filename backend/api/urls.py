from django.urls import path
from .views import movies_list,movie_detail

urlpatterns = [
    path("movies", movies_list),   # no trailing slash
    path("movies/<int:movie_id>/", movie_detail)

]
