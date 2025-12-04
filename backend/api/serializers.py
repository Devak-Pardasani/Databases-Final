from rest_framework import serializers
from .models import Movies, Genres, Actors, Directors, MovieToGenre, MovieToActor, MovieToDirector

class MovieSerializer(serializers.ModelSerializer):
    genre = serializers.SerializerMethodField()
    actors = serializers.SerializerMethodField()
    director = serializers.SerializerMethodField()

    class Meta:
        model = Movies
        fields = ['movie_id', 'title', 'runtime_min', 'rating', 'genre', 'actors', 'director']

    def get_genre(self, obj):
        """Get the genre name for this movie"""
        mtg_qs = MovieToGenre.objects.filter(movie=obj)
        
        return [mtg.genre.genre_name for mtg in mtg_qs]
        

    def get_actors(self, obj):
        """Get list of actor names for this movie"""
        mta_qs = MovieToActor.objects.filter(movie=obj).select_related('actor')
        return [mta.actor.actor_name for mta in mta_qs]

    def get_director(self, obj):
        """Get the director name for this movie"""
        mtd = MovieToDirector.objects.filter(movie=obj).first()
        if mtd and mtd.director:
            return mtd.director.director_name
        return None