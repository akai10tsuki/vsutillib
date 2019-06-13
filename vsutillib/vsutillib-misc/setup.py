"""
setup for vsutillib-misc
"""

import io
import os
import shutil
import sys

from pathlib import Path
from setuptools import setup

from vsutillib import config

sys.path.insert(0, os.path.abspath('../..'))

ROOT = os.path.abspath(os.path.dirname(__file__))
PACKAGE = "misc"


def removeBuild():
    """
    delete build directory setup was including files from other builds
    """
    b = Path('build')

    if b.is_dir():
        shutil.rmtree('build')


def readme():
    """get README.rst"""

    try:
        with io.open(os.path.join(ROOT, 'README.rst'), encoding='utf-8') as f:
            long_description = '\n' + f.read()
    except FileNotFoundError:
        long_description = "vsutillib." + PACKAGE + " sub package part of vsutillib"
    return long_description


removeBuild()

setup(
    name=config.NAME + '-' + PACKAGE,
    version='1.0.1.post1',
    description="vsutillib." + PACKAGE + " sub package part of vsutillib",
    long_description=readme(),
    author=config.AUTHOR,
    author_email=config.EMAIL,
    license='MIT',
    packages=['vsutillib.' + PACKAGE, 'vsutillib.' + PACKAGE + '.classes'],
    zip_safe=False,
)
