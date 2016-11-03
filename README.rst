pymiparse
=========

pymiparse is an easy to use parser for MediaInfo text logs.
Most current MediaInfo parsing libraries for Python either act as straight wrappers around
the MediaInfo binary or are only capable of translating XML output from MediaInfo.

In addition, pymiparse is capable of automatically parsing and identifying the following in a developer-friendly format,
so that developers don't have to:

- All MediaInfo sections (General, Audio, Video, Text, Menu)
- Filename and container
- Primary video codec
- Primary audio codec
- Common audio channel configurations (1.0, 2.0, 2.1, 5.1, 7.1)
- All audio languages
- All subtitle languages
- And more!

pymiparse is powerful and easy to use::

    >>> import pymiparse
    >>> with open('mediainfo_log.txt', 'r') as f:
    ...     logs = pymiparse.parse_from_file(f)
    ...
    >>> logs[0].get_primary_video_codec()
    'H.264'
    >>> logs[0].get_primary_audio_codec()
    'AAC'
    >>> logs[0].get_primary_audio_channels()
    '2.0'
    >>> logs[0].get_audio_languages()
    ['Japanese']
    >>> logs[0].get_subtitle_languages()
    ['English', 'Japanese']

Installing
----------

pymiparse can be installed with `pip <https://pip.pypa.io>`_::

    $ pip install pymiparse

Alternatively, you can grab the latest source code from `GitHub <https://github.com/wchill/pymiparse>`_::

    $ git clone git://github.com/wchill/pymiparse.git
    $ python setup.py install


Documentation
-------------

To be completed...


Contributing
------------

To be completed...

Maintainers
-----------

- `@wchill <https://github.com/wchill>`_ (Eric Ahn)

