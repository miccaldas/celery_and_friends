"""Module Docstring"""
import subprocess

import isort  # noqa: F401
import snoop
from loguru import logger
from kombu import Connection
from __init__ import app
from tasks import default_browser
from kombu import Connection, Producer, Exchange

fmt = "{time} - {name} - {level} - {message}"
logger.add("../logs/info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)  # noqa: E501
logger.add("../logs/error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)  # noqa: E501

subprocess.run(["isort", __file__])


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])

broker_url = "redis://localhost:6379/0"


@logger.catch
@snoop
def trigger():
    """"""
    connection = Connection("redis://localhost:6379/0")
    with connection as conn:
        with conn.channel() as channel:
            producer = Producer(channel)
    r = default_browser.delay()
    retry = (True,)
    producer.publish(r, serializer="json")
    print(r.successful())
    print(r.state)
    print(r.get())


if __name__ == "__main__":
    trigger()
