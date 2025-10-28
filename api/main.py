from pathlib import Path

from celery.result import AsyncResult
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel

from api.crud import crud_error_message, crud_get_user, crud_get_weather
from api.database import engine
from api.tasks import task_add_user, task_add_weather

# ---------------------------------------------------------------------
# Environment Setup
# ---------------------------------------------------------------------

# Load environment variables from parent directory (.env at project root)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Ensure DB tables are created
SQLModel.metadata.create_all(engine)

# Initialize FastAPI app
app = FastAPI()


# ---------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------

@app.get("/")
def read_root():
    """Root endpoint for health check."""
    return {"Alperen": "Cubuk"}


# ---------------------------------------------------------------------
# User Endpoints
# ---------------------------------------------------------------------


@app.post("/users/{count}/{delay}", status_code=201)
def add_user(count: int, delay: int):
    """
    Fetch random users and insert them asynchronously using Celery.
    Redis is used as the broker, Postgres as the backend.
    """
    task = task_add_user.delay(count, delay)
    return {"task_id": task.id}


@app.post("/users/{count}", status_code=201)
def add_user_default_delay(count: int):
    """
    Same as /users/{count}/{delay} but uses a default 10s delay.
    """
    return add_user(count, 10)


@app.get("/users/{user_id}")
def get_user(user_id: int):
    """Fetch a specific user from the database."""
    user = crud_get_user(user_id)
    if user:
        return user
    raise HTTPException(404, crud_error_message(f"No user found for id: {user_id}"))


# ---------------------------------------------------------------------
# Weather Endpoints
# ---------------------------------------------------------------------

@app.post("/weathers/{city}/{delay}", status_code=201)
def add_weather(city: str, delay: int):
    """
    Fetch weather data for a city and insert asynchronously using Celery.
    Redis is used as the broker, Postgres as the backend.
    """
    task = task_add_weather.delay(city, delay)
    return {"task_id": task.id}


@app.post("/weathers/{city}", status_code=201)
def add_weather_default_delay(city: str):
    """
    Same as /weathers/{city}/{delay} but uses a default 10s delay.
    """
    return add_weather(city, 10)


@app.get("/weathers/{city}")
def get_weather(city: str):
    """Fetch weather information from the database."""
    weather = crud_get_weather(city.lower())
    if weather:
        return weather
    raise HTTPException(404, crud_error_message(f"No weather found for city: {city}"))


# ---------------------------------------------------------------------
# Task Status Endpoint
# ---------------------------------------------------------------------

@app.get("/tasks/{task_id}")
def task_status(task_id: str):
    """
    Retrieve Celery task status.
    Possible states:
    - PENDING
    - STARTED
    - SUCCESS
    - FAILURE
    - RETRY
    - REVOKED
    """
    task = AsyncResult(task_id)
    state = task.state

    if state == "FAILURE":
        return {"state": state, "error": str(task.result)}

    return {"state": state}
