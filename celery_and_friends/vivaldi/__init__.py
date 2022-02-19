from celery import Celery
from celery.schedules import crontab

app = Celery(
    "vivaldi",
    broker_url="redis://localhost:6379/0",
    result_backend="redis://localhost:6379/0",
    imports=["tasks"],
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Lisbon",
)
beat_schedule = {
    "set_default": {
        "task": "tasks.default_browser",
        "schedule": crontab(minute=0, hour=1),
        "args": (),
    },
}

if __name__ == "__main__":
    app.start()
