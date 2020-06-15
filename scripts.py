import os
import sys
from pathlib import Path
from subprocess import CalledProcessError, check_call

from loguru import logger

ROOT = Path(__file__).parent
files = ["labeltext/", "scripts.py"]


def _call(cmd, options=[]) -> None:
    command = cmd.split(" ") + options
    logger.info(f">>>>>>>>     {' '.join(command)}")
    try:
        os.chdir(ROOT)
        check_call(command)
    except CalledProcessError as ex:
        print(f"[FAIL]  {ex}")
        sys.exit(2)
    logger.info("<<<<<<<<<< ")


def fix() -> None:
    _call("isort", ["-rc", "-l 120"] + files)
    _call("black", files)
    _call("flake8", files)
