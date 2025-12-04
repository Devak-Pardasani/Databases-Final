from django.core.management.base import BaseCommand
from api.models import Movies, Genres, MovieToGenre

class Command(BaseCommand):
    help = "Simple CLI to interact with the MovieDB"

    def handle(self, *args, **kwargs):
        while True:
            print("\n--- MovieDB CLI ---")
            print("1. List all movies")
            print("2. Find movies by genre")
            print("3. Quit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.list_movies()
            elif choice == "2":
                genre_name = input("Enter genre name: ")
                self.movies_by_genre(genre_name)
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice, try again.")

    def list_movies(self):
        movies = Movies.objects.all()
        for m in movies:
            print(f"ID: {m.movie_id}, Title: {m.title}, Runtime: {m.runtime_min}, Rating: {m.rating}")

    def movies_by_genre(self, genre_name):
        genre = Genres.objects.filter(genre_name=genre_name).first()
        if not genre:
            print(f"No genre found with name '{genre_name}'")
            return

        movie_links = MovieToGenre.objects.filter(genre=genre)
        for link in movie_links:
            print(f"ID: {link.movie.movie_id}, Title: {link.movie.title}")
