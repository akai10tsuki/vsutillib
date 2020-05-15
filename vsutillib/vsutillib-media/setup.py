"""
setup for vsutillib-media
"""

import io
import os
import shutil
import sys

from pathlib import Path
from setuptools import setup

from vsutillib import config

sys.path.insert(0, os.path.abspath("../.."))

ROOT = os.path.abspath(os.path.dirname(__file__))
PACKAGE = "media"


def removeTmpDirs():
    """
    delete build directory setup was including files from other builds
    """
    p = Path(".")
    eggDirs = [x for x in p.glob("*.egg-info") if x.is_dir()]
    eggDirs.append(Path("build"))

    for d in eggDirs:
        if d.is_dir():
            shutil.rmtree(d)


def readme():
    """get README.rst"""

    try:
        with io.open(os.path.join(ROOT, "README.rst"), encoding="utf-8") as f:
            long_description = "\n" + f.read()
    except FileNotFoundError:
        long_description = "vsutillib." + PACKAGE + " sub package part of vsutillib"
    return long_description


setup(
    name=config.NAME + "-" + PACKAGE,
    version=config.MEDIA_VERSION,
    description="vsutillib." + PACKAGE + " sub package part of vsutillib",
    long_description=readme(),
    author=config.AUTHOR,
    author_email=config.EMAIL,
    license="MIT",
    packages=["vsutillib." + PACKAGE, "vsutillib." + PACKAGE + ".classes"],
    install_requires=["pymediainfo>" + config.PYMEDIAINFO_VERSION],
    zip_safe=False,
    python_requires=config.PYTHON_VERSION,
)

removeTmpDirs()
