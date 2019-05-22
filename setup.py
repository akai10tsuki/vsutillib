#!/usr/bin/env python
# -*- coding: utf-8 -*-"""Setup.py for vsutillib"""

"""setup file to build python distributions"""


import io
import os

from setuptools import setup, find_packages

from vsutillib import config


ROOT = os.path.abspath(os.path.dirname(__file__))

def readme():
    """get README.rst"""

    try:
        with io.open(os.path.join(ROOT, 'README.rst'), encoding='utf-8') as f:
            long_description = '\n' + f.read()
    except FileNotFoundError:
        long_description = config.DESCRIPTION
    return long_description

setup(

    name=config.NAME,  # Required
    version=config.VERSION,  # Required
    description=config.DESCRIPTION,  # Required
    long_description=readme(),  # Optional
    author='Efrain Vergara',  # Optional
    author_email='akai10tsuki@gmail.com',  # Optional
    url=config.URL,
    license='MIT',

    classifiers=[  # Optional
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers

        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Video',
        'Topic :: Software Development :: Libraries',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Operating Systems
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Operating System :: POSIX :: Linux',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        # Implementation
        "Programming Language :: Python :: Implementation :: CPython",
    ],

    keywords=config.KEYWORDS,  # Optional

    packages=find_packages(exclude=['docs', 'tests*',]),  # Required

    install_requires=config.REQUIRED,

    python_requires='>=3.5, <4',

    include_package_data=True,

    entry_points={  # Optional
        'console_scripts': [
            'apply2files=vsutillib:apply2files'
            'dsf2wv=vsutillib:dsf2wv',
            'mkvrun=vsutillib:mkvrun',
        ],
    },

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/akai10tsuki/vsutillib/issues',
        'Source': 'https://github.com/akai10tsuki/vsutillib/',
    },
)
