# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is enabled on this template. See [this documentation](https://react.dev/learn/react-compiler) for more information.

Note: This will impact Vite dev & build performances.

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.

## Running the Frontend

npm run dev

## Setting up Backend

1) Install PostgreSQL and required dependancies
    pip install -r requirements.txt
2) Create env. file
    DATABASE_NAME=moviedb
    DATABASE_USER=csds341group
    DATABASE_PASSWORD=password
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
3) Create Local Database and Load SQL Schema
- psql -U postgres OR & "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres
- CREATE USER csds341group WITH PASSWORD 'password';
- CREATE DATABASE moviedb OWNER csds341group;
- psql -U csds341group -d moviedb -f <path_to_MovieDB.sql>
4) Run in terminal:
- python manage.py makemigrations
- python manage.py migrate
5) Run Server
- python manage.py runserver
