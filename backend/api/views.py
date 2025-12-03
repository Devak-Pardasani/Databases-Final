from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Movies
from .serializers import MovieSerializer

@api_view(["GET", "POST"])
def movies_list(request):

    # GET → return all movies
    if request.method == "GET":
        movies = Movies.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    # POST → create a new movie
    if request.method == "POST":
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
