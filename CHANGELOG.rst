Changelog
=========

(Unreleased)
~~~~~~~~~~~~

Changed
*******

- modify files to bump version to 1.5.0
- Using some Python 3.8 specific features drop support versions less than 3.8

files package
~~~~~~~~~~~~~

Added
*****

- getDirectoryList function like getFilesList for directories
  accepts wildcard on directory arguments

Changed
********
- block drag & drop when files added programmatically
- getFilesList accepts wildcard on directory argument
- getFilesList changed default wildcard to '*' from '*.*'

Fixed
******


pyqt package
~~~~~~~~~~~~

Added
*****

- centerWidgets function
- QThreads classes

Changed
*******

- To use this package Python version has to be 3.8.1 PySide2 does not support
  version 3.8

Fixed
*****

- shortcut handling on QActionWidget


mkv package
~~~~~~~~~~~

Added:
******
- add property for chaptersFile (pathlib.Path)

Changed:
********
- VerifyStructure provides more details

Fixed:
******
- fix handling of files with single quotes

scripts
-------

Changed
*******

- dsf2wv accepts wildcard on directory argument
- apply2files accepts wildcard on directory argument

2019-6-13
~~~~~~~~~

First Release

.. _RTD: https://vsutillib.readthedocs.io
