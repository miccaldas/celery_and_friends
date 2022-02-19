"""
We'll build a Celery task queue system to replace
cron, hopefully, for something a little less
nervous.
"""

import subprocess

import isort  # noqa: F401
import snoop
from loguru import logger

from __init__ import app

fmt = "{time} - {name} - {level} - {message}"
logger.add("../logs/info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)  # noqa: E501
logger.add("../logs/error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)  # noqa: E501

subprocess.run(["isort", __file__])


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


@app.task(name="default", bind=True)
@logger.catch
@snoop
def default_browser():
    """
    We'll use a bash script I had already made. that at
    every reboot, it would send a message to
    xdg-settings, saying that the default browser is
    Vivaldi. Firefox is always trying to worm itself
    to that position.
    """

    cmd = "xdg-settings set default-web-browser vivaldi-stable.desktop"
    subprocess.run(cmd, shell=True)
    with open("checker.txt", "w") as f:
        f.write("subprocess has run")


if __name__ == "__main__":
    default_browser()
