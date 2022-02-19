"""Module Docstring"""
import subprocess

import isort  # noqa: F401
import snoop
from loguru import logger

import procrastinate

fmt = "{time} - {name} - {level} - {message}"
logger.add("../logs/info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)  # noqa: E501
logger.add("../logs/error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)  # noqa: E501

subprocess.run(["isort", __file__])


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])

app = procrastinate.App(connector=procrastinate.AiopgConnector())


@app.task(queue="proc")
@logger.catch
@snoop
def proc():
    """"""
    with open("proc_file.txt", "w") as f:
        f.write("By Jove! It works!")


if __name__ == "__main__":
    proc()


with app.open():
    proc.defer()
