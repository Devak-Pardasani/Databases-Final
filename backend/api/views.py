from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import (
    Movies, 
    Genres, 
    Actors, 
    Directors, 
    MovieToGenre, 
    MovieToActor, 
    MovieToDirector
)
from .serializers import MovieSerializer

@api_view(["GET", "POST"])
def movies_list(request):

    # GET → return all movies
    if request.method == "GET":
        movies = Movies.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    # POST → create a new movie with related data
    if request.method == "POST":
        data = request.data

        with transaction.atomic():  # ensure all-or-nothing

            # Create the movie first
            movie = Movies.objects.create(
                title=data.get('title'),
                runtime_min=data.get('runtime_min'),
                rating=data.get('rating')
            )

            # Handle genre
            genre_list = data.get('genre',[])
            for genre_name in genre_list:

                if genre_name:
                    genre, _ = Genres.objects.get_or_create(genre_name=genre_name)
                    mtg = MovieToGenre(movie=movie, genre=genre)
                    mtg.save(force_insert=True)  # avoid id issue

            # Handle actors
            actors_list = data.get('actors', [])
            for actor_name in actors_list:
                if actor_name:
                    actor, _ = Actors.objects.get_or_create(actor_name=actor_name)
                    mta = MovieToActor(movie=movie, actor=actor)
                    mta.save(force_insert=True)  # avoid id issue

            # Handle director
            director_name = data.get('director')
            if director_name:
                director, _ = Directors.objects.get_or_create(director_name=director_name)
                mtd = MovieToDirector(movie=movie, director=director)
                mtd.save(force_insert=True)  # avoid id issue

        # Return the created movie with all related data
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(["GET", "DELETE"])
def movie_detail(request, movie_id):
    if request.method == "GET":
        try:
            movie = Movies.objects.get(id=movie_id)
        except Movies.DoesNotExist:
            return Response({"error": "Movie not found"}, status=404)

        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    if request.method == "DELETE":
        try:
            movie = Movies.objects.get(movie_id=movie_id)
        except Movies.DoesNotExist:
            return Response({"error": "Movie not found"}, status=404)

        with transaction.atomic():
            MovieToGenre.objects.filter(movie=movie).delete()
            MovieToActor.objects.filter(movie=movie).delete()
            MovieToDirector.objects.filter(movie=movie).delete()

            movie.delete()

        return Response({"message": f"Movie {movie_id} deleted"}, status=200)
