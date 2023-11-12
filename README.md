# M2
TeamProject23/M2

# How to

## Running the project
- Copy .env.sample into .env and populate it with custom entries
- Run the project

    `docker compose up --build`

## Database

### Migrations

- Create migration file
    
    If you have created **new table** make sure to import it in **src/models/\_\_init\_\_.py**. This way alembic will include it in revision.

    `from .user import User`

    Then, create migration files.

    `docker compose run backend alembic revision --autogenerate -m "revision message"`

    For example

    `docker compose run backend alembic revision --autogenerate -m "Add user table"`

- Run migrations, it runs automatically before web server starts


    `docker compose run backend alembic upgrade head`


- If you want to start fresh with migrations and database, run

    `docker system prune`

    and to be sure

    `docker volume prune`


    **WARNING** it deletes all images, cache and other docker stuff

### Creating super user

- While docker is running

    `docker compose run backend python3 manage.py create_admin`