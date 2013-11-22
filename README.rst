restructuredtext-lint
=====================

.. image:: https://travis-ci.org/twolfson/restructuredtext-lint.png?branch=master
   :target: https://travis-ci.org/twolfson/restructuredtext-lint
   :alt: Build Status

`reStructuredText`_ `linter`_

This was created out of frustration with `PyPI`_; it sucks finding out your `reST`_ is invalid **after** uploading it. It is being developed in junction with a `Sublime Text`_ linter.

.. _`reStructuredText`: http://docutils.sourceforge.net/rst.html
.. _`linter`: http://en.wikipedia.org/wiki/Lint_%28software%29
.. _`reST`: _`reStructuredText`
.. _`PyPI`: http://pypi.python.org/
.. _`Sublime Text`: http://sublimetext.com/

Getting Started
---------------
Install the module with: ``pip install restructuredtext_lint``

.. code:: python

    import restructuredtext_lint
    errors = restructuredtext_lint.lint("""
    Hello World
    =======
    """)

    # `errors` will be list of system messages
    # [<system_message: <paragraph...><literal_block...>>]
    errors[0].message  # Title underline too short.

Documentation
-------------
``restructuredtext-lint`` exposes a ``lint`` function

``restructuredtext_lint.lint(content, filepath=None)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Lint `reStructuredText`_ and return errors

- content `String` - `reStructuredText`_ to be linted
- filepath `String` - Optional path to file, this will be returned as the source

Returns:

- errors `List` - List of errors
    - Each error is a class from `docutils`_ with the following attrs
        -

.. _`docutils`: http://docutils.sourceforge.net/

Examples
--------
_(Coming soon)_

Contributing
------------
In lieu of a formal styleguide, take care to maintain the existing coding style. Add unit tests for any new or changed functionality. Test via ``nosetests``.

Donating
--------
Support this project and `others by twolfson`_ via `gittip`_.

.. image:: https://rawgithub.com/twolfson/gittip-badge/master/dist/gittip.png
   :target: `gittip`_
   :alt: Support via Gittip

.. _`others by twolfson`:
.. _gittip: https://www.gittip.com/twolfson/

Unlicense
---------
As of Nov 22 2013, Todd Wolfson has released this repository and its contents to the public domain.

It has been released under the `UNLICENSE`_.

.. _UNLICENSE: https://github.com/twolfson/restructuredtext-lint/blob/master/UNLICENSE
