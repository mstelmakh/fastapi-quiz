# Quiz
This application provides RESTful API for creating, completing and review quizzes.

## General
Anonymous user can:
- Sign Up
- Log In
- Retrieve list of all quizzes

Only logged in users can:
- Create quiz
- Create questions for created quizzes
- Create choices for created questions
- Retrieve detail of particular quiz
- Retrieve questions of particular quiz
- Retrieve available choices for particular question of the quiz
- Try to complete the quiz
- Answer to questions during solving the quiz
- Submit the attempt
- Retrieve list of attempts made by the user

## Technologies used

- FastAPI
- PostgreSQL
- Docker
- JWT
- SQLAlchemy
- alembic
- pytest

## Setting environment variables

Application settings are set based on environment variables, but if such variables are not set, the settings are read from the `.env` (`.env.docker` if using docker-compose) file.

Example `.env` file:
```
POSTGRES_USER=testuser
POSTGRES_PASSWORD=qwerty
POSTGRES_SERVER=localhost
POSTGRES_DB=testdb

JWT_SECRET=secret
```

### Locally
1. Override `.env` file.

2.  ```sh
    pip install -r src/requirements.txt
    python src/app/main.py
    ```

### Docker
1. Override `.env.docker` file.
2. `docker-compose up`
3. `docker-compose run --rm web sh -c "alembic upgrade head"` - to apply migrations.

## Testing

Locally:

`pytest src/tests`

Using Docker:

`docker-compose run --rm web sh -c "pytest src/tests"`
