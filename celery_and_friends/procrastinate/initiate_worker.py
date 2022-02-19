"""Module Docstring"""
import subprocess
import isort  # noqa: F401
import snoop
from loguru import logger
from proc import proc

fmt = "{time} - {name} - {level} - {message}"
logger.add("../logs/info.log", level="INFO", format=fmt, backtrace=True, diagnose=True)  # noqa: E501
logger.add("../logs/error.log", level="ERROR", format=fmt, backtrace=True, diagnose=True)  # noqa: E501

subprocess.run(["isort", __file__])


def type_watch(source, value):
    return "type({})".format(source), type(value)


snoop.install(watch_extras=[type_watch])


@logger.catch
@snoop
def initiate_worker():
    """"""
    app.run_worker(queues=["proc"])


if __name__ == "__main__":
    initiate_worker()
