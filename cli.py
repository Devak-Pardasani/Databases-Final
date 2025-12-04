import os
from dotenv import load_dotenv
import psycopg2

load_dotenv() 


DB_NAME = os.getenv("DATABASE_NAME")
DB_USER = os.getenv("DATABASE_USER")
DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
DB_HOST = os.getenv("DATABASE_HOST", "localhost")
DB_PORT = os.getenv("DATABASE_PORT", 5432)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

while True:
    print("\nMovieDB CLI")
    print("1. List all movies")
    print("2. List all genres")
    print("3. Exit.")
    choice = input("Choose an option: ")

    if choice == "1":
        cur.execute("SELECT * FROM movies;")
        rows = cur.fetchall()
        for row in rows:
            print(row)

    elif choice == "2":
        cur.execute("SELECT * FROM genres;")
        rows = cur.fetchall()
        for row in rows:
            print(row)

    elif choice == "3":
        break

    else:
        print("Invalid choice. Try again.")

cur.close()
conn.close()
