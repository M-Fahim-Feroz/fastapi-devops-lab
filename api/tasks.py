import os
import time
import requests
from celery import Celery
from api.crud import crud_add_user, crud_add_weather
from api.models import UserIn, WeatherIn


# ---------------------------------------------------------------------
# Environment-aware configuration
# ---------------------------------------------------------------------

IS_CI = os.getenv("GITHUB_ACTIONS") == "true"
IS_TEST = bool(os.getenv("PYTEST_CURRENT_TEST"))

REDIS_HOST = "localhost" if IS_CI else "redis"
DB_HOST = "localhost" if IS_CI else "database"

REDIS_URL = f"redis://{REDIS_HOST}:6379/0"
DATABASE_URL = f"db+postgresql://user:password@{DB_HOST}:5432/alpha"

# Choose backend depending on environment
if IS_CI or IS_TEST:
    RESULT_BACKEND = "cache+memory://"
else:
    RESULT_BACKEND = DATABASE_URL

# Initialize Celery application
app = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=RESULT_BACKEND,
)

# Core Celery config
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Run synchronously (eager mode) during CI or pytest
if IS_CI or IS_TEST:
    app.conf.update(
        task_always_eager=True,
        task_store_eager_result=True,
    )


# ---------------------------------------------------------------------
# Celery Tasks
# ---------------------------------------------------------------------


@app.task
def task_add_user(count: int, delay: int):
    """Fetch random user data and add them to the database."""
    url = "https://randomuser.me/api"
    try:
        response = requests.get(f"{url}?results={count}", timeout=10)
        response.raise_for_status()
        data = response.json()["results"]
    except Exception as e:
        return {"error": f"Failed to fetch user data: {e}"}

    time.sleep(delay)
    result = []

    for item in data:
        user = UserIn(
            first_name=item["name"]["first"],
            last_name=item["name"]["last"],
            mail=item["email"],
            age=item["dob"]["age"],
        )
        if crud_add_user(user):
            result.append(user.dict())

    return {"success": result, "inserted": len(result)}


@app.task
def task_add_weather(city: str, delay: int):
    """Fetch weather data for the specified city and insert into database."""
    url = f"https://api.collectapi.com/weather/getWeather?data.lang=tr&data.city={city}"
    headers = {
        "content-type": "application/json",
        "authorization": "apikey 4HKS8SXTYAsGz45l4yIo9P:0NVczbcuJfjQb8PW7hQV48",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()["result"]
    except Exception as e:
        return {"error": f"Failed to fetch weather data: {e}"}

    time.sleep(delay)
    result = []

    for item in data:
        weather = WeatherIn(
            city=city.lower(),
            date=item["date"],
            day=item["day"],
            description=item["description"],
            degree=item["degree"],
        )
        if crud_add_weather(weather):
            result.append(weather.dict())

    return {"success": result, "inserted": len(result)}
