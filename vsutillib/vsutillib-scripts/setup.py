"""
setup for vsutillib-file
"""

import io
import os
import sys

from setuptools import setup

from vsutillib import config

sys.path.insert(0, os.path.abspath('../..'))

ROOT = os.path.abspath(os.path.dirname(__file__))
PACKAGE = "scripts"


def readme():
    """get README.rst"""

    try:
        with io.open(os.path.join(ROOT, 'README.rst'), encoding='utf-8') as f:
            long_description = '\n' + f.read()
    except FileNotFoundError:
        long_description = "vsutillib." + PACKAGE + " sub package part of vsutillib"
    return long_description


setup(
    name=config.NAME + '-' + PACKAGE,
    version='1.0.1',
    description="vsutillib." + PACKAGE + " sub package part of vsutillib",
    long_description=readme(),
    author=config.AUTHOR,
    author_email=config.EMAIL,
    license='MIT',
    packages=['vsutillib.' + PACKAGE],
    install_requires=[
        'vsutillib-files>=1.0.0',
        'vsutillib-media>=1.0.0',
        'vsutillib-mkv>=1.0.0',
        'vsutillib-process>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'vsutillib-apply2files=vsutillib:scripts.apply2files',
            'vsutillib-dsf2wv=vsutillib:scripts.dsf2wv',
            'vsutillib-mkvrun=vsutillib:scripts.mkvrun',
        ],
    },
    python_requires='>=3.5, <4',
    zip_safe=False,
)
