import psycopg2
import argparse
from dotenv import load_dotenv
import os
load_dotenv()

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DATABASE_NAME'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            host=os.getenv('DATABASE_HOST'),
            port=os.getenv('DATABASE_PORT')
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None
    
def add_movie(conn, title, rating, genre=None, actor=None, runtime_min=None, director=None):
    cur = conn.cursor()

    insert_movie_query = """
        INSERT INTO Movies (title, runtime_min, rating)
        VALUES (%s, %s, %s)
        RETURNING movie_id;
    """
    cur.execute(insert_movie_query, (title, runtime_min, rating))
    movie_id = cur.fetchone()[0]
    print(f"Movie added with ID {movie_id}")

    if genre: # Check genre stuff
        if isinstance(genre, str):
            genre = [genre]
        for g in genre:
            cur.execute("""
                INSERT INTO Genres (genre_name)
                VALUES (%s)
                RETURNING genre_id;
            """, (g,))
            row = cur.fetchone()
            if row is None:
                cur.execute("SELECT genre_id FROM Genres WHERE genre_name = %s;", (g,))
                row = cur.fetchone()
            genre_id = row[0]
            cur.execute(
                "INSERT INTO MovieToGenre (movie_id, genre_id) VALUES (%s, %s);",
                (movie_id, genre_id)
            )
    if actor: # Check actor stuff
        if isinstance(actor, str):  
            actor = [actor]
        for a in actor:
            cur.execute("""
                INSERT INTO Actors (actor_name)
                VALUES (%s)
                RETURNING actor_id;
            """, (a,))
            row = cur.fetchone()
            if row is None:
                cur.execute("SELECT actor_id FROM Actors WHERE actor_name = %s;", (a,))
                row = cur.fetchone()
            actor_id = row[0]
            cur.execute(
                "INSERT INTO MovieToActor (movie_id, actor_id) VALUES (%s, %s);",
                (movie_id, actor_id)
            )
    if director: # Check director stuff
        if isinstance(director, str):
            director = [director]
        for d in director:
            cur.execute("""
                INSERT INTO Directors (director_name)
                VALUES (%s)
                RETURNING director_id;
            """, (d,))
            row = cur.fetchone()
            if row is None:
                cur.execute("SELECT director_id FROM Directors WHERE director_name = %s;", (d,))
                row = cur.fetchone()
            director_id = row[0]
            cur.execute(
                "INSERT INTO MovieToDirector (movie_id, director_id) VALUES (%s, %s);",
                (movie_id, director_id)
            )

    conn.commit()
    cur.close()

def view_movies(conn):
    cur = conn.cursor()
    query = """
    SELECT 
        m.movie_id,
        m.title,
        m.runtime_min,
        m.rating,
        array_agg(DISTINCT g.genre_name) AS genres,
        array_agg(DISTINCT a.actor_name) AS actors,
        array_agg(DISTINCT d.director_name) AS directors
    FROM Movies m
    LEFT JOIN MovieToGenre mtg ON m.movie_id = mtg.movie_id
    LEFT JOIN Genres g ON mtg.genre_id = g.genre_id
    LEFT JOIN MovieToActor mta ON m.movie_id = mta.movie_id
    LEFT JOIN Actors a ON mta.actor_id = a.actor_id
    LEFT JOIN MovieToDirector mtd ON m.movie_id = mtd.movie_id
    LEFT JOIN Directors d ON mtd.director_id = d.director_id
    GROUP BY m.movie_id, m.title, m.runtime_min, m.rating
    ORDER BY m.movie_id;
    """
    cur.execute(query)
    rows = cur.fetchall()
    display_rows(rows, [desc[0] for desc in cur.description])
    cur.close()

def view_genres(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM genres;")
    rows = cur.fetchall()
    display_rows(rows, [desc[0] for desc in cur.description])
    cur.close()

def view_actors(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM actors;")
    rows = cur.fetchall()
    display_rows(rows, [desc[0] for desc in cur.description])
    cur.close()

def view_directors(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM directors;")
    rows = cur.fetchall()
    display_rows(rows, [desc[0] for desc in cur.description])
    cur.close()

def execute_query(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    results = cur.fetchall()
    cur.close()
    return results

def display_rows(rows, column_names): # Print tables nicely
    col_widths = [max(len(str(col)), 12) for col in column_names]
    for i, col in enumerate(column_names):
        max_data_width = max((len(str(row[i])) for row in rows), default=0)
        col_widths[i] = max(col_widths[i], max_data_width)
    header = " | ".join(f"{name:<{col_widths[i]}}" for i, name in enumerate(column_names))
    print(header)
    print("-" * len(header))
    for row in rows:
        row_display = [
            ", ".join(r) if isinstance(r, list) else str(r) for r in row
        ]
        print(" | ".join(f"{row_display[i]:<{col_widths[i]}}" for i in range(len(row_display))))


def main():
    parser = argparse.ArgumentParser(description="PostgreSQL Movie Database CLI")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add Movie
    add_movie_parser = subparsers.add_parser("add-movie", help="Add a new movie")
    add_movie_parser.add_argument("-t", "--title", required=True, help="Movie title")
    add_movie_parser.add_argument("-ra", "--rating", type=int, required=True, help="Movie rating (1-10)")
    add_movie_parser.add_argument("-ru", "--runtime", type=int, help="Runtime in minutes")
    add_movie_parser.add_argument("-g", "--genre", nargs="*", help="Genre(s)")
    add_movie_parser.add_argument("-a", "--actor", nargs="*", help="Actor(s)")
    add_movie_parser.add_argument("-d", "--director", nargs="*", help="Director(s)")

    # View Movie
    subparsers.add_parser("view-movies", help="View all movies")

    # View Other Tables
    subparsers.add_parser("view-genres", help="View all genres")
    subparsers.add_parser("view-directors", help="View all directors")
    subparsers.add_parser("view-actors", help="View all actors")

    # Sql injection :)
    query_parser = subparsers.add_parser("query", help="Execute raw SQL")
    query_parser.add_argument("sql", help="SQL query to execute")


    args = parser.parse_args()
    conn = connect_to_db()

    if args.command == "add-movie":
        add_movie(
            conn,
            title=args.title,
            rating=args.rating,
            runtime_min=args.runtime,
            genre=args.genre,
            actor=args.actor,
            director=args.director
        )
    elif args.command == "view-movies":
        view_movies(conn)
    elif args.command == "view-genres":
        view_genres(conn)
    elif args.command == "view-actors":
        view_actors(conn)
    elif args.command == "view-directors":
        view_directors(conn)
    elif args.command == "query":
        results = execute_query(conn, args.sql)
        for r in results:
            print(r)

if __name__ == "__main__":
    main()  


"""
Example Commands

1. Add a new movie
python cli.py add-movie --title "Inception" --rating 9 --runtime 190 --genre Sci-Fi --actor "Joseph Gordon-Levitt" --director "Christopher Nolan"

2. View all movies
python cli.py view-movies

3. View all genres
python cli.py view-genres

4. View all actors
python cli.py view-actors

5. View all directors
python cli.py view-directors

6. Execute a raw SQL query
python cli.py query "SELECT title, rating FROM Movies WHERE rating >= 8 ORDER BY rating DESC;"
"""