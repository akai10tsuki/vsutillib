
****************************************************
vsutillib: module with utility functions and classes
****************************************************


.. image:: https://img.shields.io/pypi/v/vsutillib.svg
  :target: https://pypi.org/project/vsutillib

.. image:: https://img.shields.io/pypi/pyversions/vsutillib.svg
  :target: https://pypi.org/project/vsutillib


These are a collection of functions and classes that I use on
my applications to made easier to maintain I decided to release
it and install as a dependency of apps like mkvbatchmultiplex.

Description
===========

A range of functions and classes with a variety of uses for
example:

 - functions
   * getFileList - return the files on a directory in
     **list** of pathlib.Path objects
   * findFile - find a file in the system Path
     return a pahtlib.Path object if found
   * getExecutable - find executable file
     in PATH and the normal installation paths for Windows
     and macOS for linux is like findFile
 - classes
   * RunCommand - execute command in subprocess and capture
     output optionally apply regular expression searches
     and apply a supplied function to receive every line
     read and process them as needed
   * ConfigurationSettings - maintain a set of ConfigurationSettings
     in a **dictionary** and saved it in xml file
 - utilities
   * dsf2wv - compresses DSF audio files to WavPack compressed
     files
   * mkvbatchrun - CLI utility to execute MKVToolNix_ generated
     command line.  MKVBatchMultiplex_ is a GUI implementation
     of this and the main reason this module goes public.

and so on...

Installation
============

.. code:: bash

    pip install vsutillib

Main development platform is Windows but the majority of functions
work on Linux and macOS.  Some are OS specific like isDarkMode that
detect if macOS Mojave is running in Dark Mode.  If the function is
run on Linux or Windows always returns **False**.

Dependencies
************

    * lxml_ 4.3.3 or greater on system
      XmlDB simple xml database
    * pymediainfo_ 4.0 or greater
      MediaFileInfo depends on it
    * Python_ 3.5 or greater
    * MediaInfo_ tested with versions 17.10->18.12
      this only for Linux a dependecy of pymediainfo
    * WavPackMKVToolNix_ tested with versions 17.00->34.0.0
      mkvbatchrun depends on it
    * WavPack_ file compressor 5.1.0 or greater
      dsf2wv depends on it

For now is a python package it can be installed:

::

    pip install vsutillib
    or download the source


macOS 10.14 Dark theme MKVToolNix has to be version 30.0.0+

Usage
=====

Mainly for programmers there are some utility modules like DSF to WavPack.
So python knowledge is needed:

file make any operations needed copy command to clipboard:

    *Multiplexer->Show command line*

Paste command on mkvbatchmultiplex push Process button and wait.
Remember to select and output directory.

Roadmap
=======

This is just the base for the project.  The roadmap is:

    * Work on a stable release.
    * Easier installation for different operating systems
    * Documentation
    * Work on job queue management

The application works for me as is. If the the program generates any interest
any further changes and additions will depend on user base needs.

Work on binaries started.

See https://mkvbatchmultiplex.readthedocs.io for more information.

.. Hyperlinks.

.. _pymediainfo: https://pypi.org/project/pymediainfo/
.. _Python: https://www.python.org/downloads/
.. _MKVToolNix: https://mkvtoolnix.download/
.. _Matroska: https://www.matroska.org/
.. _MediaInfo: https://mediaarea.net/en/MediaInfo
.. _AVI: https://docs.microsoft.com/en-us/windows/desktop/directshow/avi-file-format/
.. _SRT: https://matroska.org/technical/specs/subtitles/srt.html
.. _MKVBatchMultiplex: https://github.com/akai10tsuki/mkvbatchmultiplex
.. _WavPack: http://www.wavpack.com/
