Changelog
=========

(Unreleased)
~~~~~~~~~~~~

Changed
********
- modify files to bump version to 1.5.0
 - Using Python 3.8 features drop support for 3.5->3.8

pyqt
----

Added

- centerWidgets function

files
-----

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

mkv
---

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
