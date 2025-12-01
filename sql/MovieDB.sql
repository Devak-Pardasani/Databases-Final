-- psql -u postgres
-- CREATE DATABASE MovieDB;
-- psql -U postgres -d MovieDB -f path/to/MovieDB.sql

CREATE Table Movies (
    movie_id SERIAL primary key,
    title VARCHAR(255) not null,
    runtime_min INT,
    rating INT
);

CREATE Table Genres (
    genre_id SERIAL primary key,
    genre_name VARCHAR(255) not null
);

CREATE Table MovieToGenre(
    movie_id INT references movies(movie_id),
    genre_id INT references genres(genre_id),
    primary key (movie_id, genre_id)
);

CREATE Table Actors (
    actor_id SERIAL primary key,
    actor_name VARCHAR(255) not null
);

CREATE Table MovieToActor(
    movie_id INT references movies(movie_id),
    actor_id INT references actors(actor_id),
    character_name VARCHAR(255),
    primary key (movie_id, actor_id)
);

CREATE Table Directors (
    director_id SERIAL primary key,
    director_name VARCHAR(255) not null
);

CREATE Table MovieToDirector(
    movie_id INT references movies(movie_id),
    director_id INT references directors(director_id),
    primary key (movie_id, director_id)
);