import os
import time
import requests
from celery import Celery
from api.crud import crud_add_user, crud_add_weather
from api.models import UserIn, WeatherIn

# ---------------------------------------------------------------------
# Environment-aware configuration
# ---------------------------------------------------------------------

# Detect if we're running inside GitHub Actions
IS_CI = os.getenv("GITHUB_ACTIONS") == "true"

# Set correct hostnames for Postgres and Redis
REDIS_HOST = "localhost" if IS_CI else "redis"
DB_HOST = "localhost" if IS_CI else "database"

# Build the full broker and backend URLs
REDIS_URL = f"redis://{REDIS_HOST}:6379/0"
DATABASE_URL = f"db+postgresql://user:password@{DB_HOST}:5432/alpha"

# Initialize Celery application
app = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=DATABASE_URL,
)

# Celery configuration
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# ---------------------------------------------------------------------
# Celery Tasks
# ---------------------------------------------------------------------

@app.task
def task_add_user(count: int, delay: int):
    """
    Fetch random user data and add them to the database.
    Each result is inserted via the CRUD layer.
    """
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
    """
    Fetch weather data for the specified city from CollectAPI
    and insert it into the database.
    """
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
