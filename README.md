# M2
TeamProject23/M2

# How to

## Running the project
- Copy .env.sample file fom /env into .env files and populate it with custom entries
- Run the dev instance

    `sudo docker compose -f docker-compose-dev.yml up --build`

- Run prod instance

    `sudo docker compose -f docker-compose-prod.yml up --build`

## Database

### Migrations

- Create migration file
    
    If you have created **new table** make sure to import it in **src/models/\_\_init\_\_.py**. This way alembic will include it in revision.

    `from .user import User`

    Then, create migration files.

    `docker compose -f docker-compose-dev.yml run backend alembic revision --autogenerate -m "revision message"`

    For example

    `docker compose -f docker-compose-dev.yml run backend alembic revision --autogenerate -m "Add user table"`

- Run migrations, it runs automatically before web server starts


    `docker compose -f docker-compose-dev.yml run backend alembic upgrade head`


- If you want to start fresh with migrations and database, run

    `docker system prune`

    and to be sure

    `docker volume prune`


    **WARNING** it deletes all images, cache and other docker stuff

### Creating super user

- While docker is running

    `docker compose -f docker-compose-dev.yml run backend python3 manage.py create_admin`
