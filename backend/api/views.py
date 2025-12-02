from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Movies
from .serializers import MovieSerializer

@api_view(['GET'])
def get_movies(request):
    movies = Movies.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

