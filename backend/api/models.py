from django.db import models

class Movies(models.Model):
    movie_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    runtime_min = models.IntegerField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "movies"   # match exact SQL table name


class Genres(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(max_length=255)

    class Meta:
        db_table = "genres"


class MovieToGenre(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, db_column="movie_id")
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE, db_column="genre_id")

    class Meta:
        db_table = "movietogenre"
        unique_together = ("movie", "genre")
        managed = False  # important — table already exists!


class Actors(models.Model):
    actor_id = models.AutoField(primary_key=True)
    actor_name = models.CharField(max_length=255)

    class Meta:
        db_table = "actors"


class MovieToActor(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, db_column="movie_id")
    actor = models.ForeignKey(Actors, on_delete=models.CASCADE, db_column="actor_id")
    character_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "movietoactor"
        unique_together = ("movie", "actor")
        managed = False


class Directors(models.Model):
    director_id = models.AutoField(primary_key=True)
    director_name = models.CharField(max_length=255)

    class Meta:
        db_table = "directors"


class MovieToDirector(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, db_column="movie_id")
    director = models.ForeignKey(Directors, on_delete=models.CASCADE, db_column="director_id")

    class Meta:
        db_table = "movietodirector"
        unique_together = ("movie", "director")
        managed = False
