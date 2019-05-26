
************
Installation
************

For installation on the command line of your operating system:

.. code:: bash

    pip install mkvbatchmultiplex

The library works on CPython 3.5->3.7

Dependencies
============

Some of the functions and/or classes use the following packages:

    Python packages are installed if pip is used:

        lxml_ - library for processing XML and HTML with Python

        pymediainfo_ - Python MediaInfo wrapper

    MKVToolNix_ - The target tool from witch we get the command

    MediaInfo_ - unified display of the most relevant technical and
    tag data for video and audio files.

Besides lxml these are really dependencies of MKVBatchMultiplex application
not necessary for majority of functions and classes.  Installation of MediaInfo
is only needed on Linux.  And this is only needed for everything to work.
lxml is use by XmlDB class witch can be useful.

Known Issues
============

.. _lxml: https://lxml.de/
.. _MediaInfo: https://mediaarea.net/en/MediaInfo/
.. _MKVBatchMultiplex: https://pypi.org/project/mkvbatchmultiplex/
.. _MKVToolNix: https://mkvtoolnix.download/
.. _pymediainfo: https://pypi.org/project/pymediainfo/
