restructuredtext-lint
=====================

.. image:: https://travis-ci.org/twolfson/restructuredtext-lint.png?branch=master
   :target: https://travis-ci.org/twolfson/restructuredtext-lint
   :alt: Build Status

`reStructuredText`_ `linter`_

This was created out of frustration with `PyPI`_; it sucks finding out your `reST`_ is invalid **after** uploading it. It is being developed in junction with a `Sublime Text`_ linter.

.. _`reStructuredText`: http://docutils.sourceforge.net/rst.html
.. _`linter`: http://en.wikipedia.org/wiki/Lint_%28software%29
.. _`reST`: `reStructuredText`_
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

CLI Utility
^^^^^^^^^^^
For your convenience, we present a CLI utility ``rst-lint`` (also available as ``restructuredtext-lint``).

.. code:: bash

    $ rst-lint --help
    usage: rst-lint [-h] [--format FORMAT] [--encoding ENCODING] filepath

    Lint a reStructuredText file

    positional arguments:
      filepath         File to lint

    optional arguments:
      -h, --help            show this help message and exit
      --format FORMAT       Format of output (e.g. text, json)
      --encoding ENCODING   Encoding of the source file (e.g. utf-8)

    $ rst-lint README.rst
    WARNING README.rst:2 Title underline too short.

Documentation
-------------
``restructuredtext-lint`` exposes a ``lint`` and ``lint_file`` function

``restructuredtext_lint.lint(content, filepath=None)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Lint `reStructuredText`_ and return errors

- content ``String`` - `reStructuredText`_ to be linted
- filepath ``String`` - Optional path to file, this will be returned as the source

Returns:

- errors ``List`` - List of errors
    - Each error is a class from `docutils`_ with the following attrs
        - line ``Integer|None`` - Line where the error occurred
            - On rare occasions, this will be ``None`` (e.g. anonymous link mismatch)
        - source ``String`` - ``filepath`` provided in parameters
        - level ``Integer`` - Level of the warning
            - Levels represent 'info': 1, 'warning': 2, 'error': 3, 'severe': 4
        - type ``String`` - Noun describing the error level
            - Levels can be 'INFO', 'WARNING', 'ERROR', or 'SEVERE'
        - message ``String`` - Error message
        - full_message ``String`` - Error message and source lines where the error occurred
    - It should be noted that ``level``, ``type``, ``message``, and ``full_message`` are custom attrs added onto the original ``system_message``

.. _`docutils`: http://docutils.sourceforge.net/

``restructuredtext_lint.lint_file(filepath, encoding=None)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Lint a `reStructuredText`_ file and return errors

- filepath ``String`` - Path to file for linting
- encoding ``String`` - Encoding to read file in as
    - When ``None`` is provided, it will use OS default as provided by `locale.getpreferredencoding`_
    - The list of supported encodings can be found at http://docs.python.org/2/library/codecs.html#standard-encodings

.. _`locale.getpreferredencoding`: http://docs.python.org/2/library/locale.html#locale.getpreferredencoding

Returns: Same structure as ``restructuredtext_lint.lint``

Extension
---------
Under the hood, we leverage `docutils`_ for parsing reStructuredText documents. `docutils`_ supports adding new directives and roles via ``register_directive`` and ``register_role``. Here is an example of adding a directive from `sphinx`_.

.. _`sphinx`: http://sphinx-doc.org/

https://github.com/sphinx-doc/sphinx/blob/1.3/sphinx/directives/code.py

**sphinx.rst**

.. code:: rst

    Hello
    =====
    World

    .. highlight:: python

        Hello World!

**sphinx.py**

.. code:: python

    # Load in our dependencies
    from docutils.parsers.rst.directives import register_directive
    from sphinx.directives.code import Highlight
    import restructuredtext_lint

    # Load our new directive
    register_directive('highlight', Highlight)

    # Lint our README
    errors = restructuredtext_lint.lint_file('docs/sphinx/README.rst')
    print errors[0].message # Error in "highlight" directive: no content permitted.

Examples
--------
Here is an example of all invalid properties

.. code:: python

    rst = """
    Some content.

    Hello World
    =======
    Some more content!
    """
    errors = restructuredtext_lint.lint(rst, 'myfile.py')
    errors[0].line  # 5
    errors[0].source  # myfile.py
    errors[0].level  # 2
    errors[0].type  # WARNING
    errors[0].message  # Title underline too short.
    errors[0].full_message  # Title underline too short.
                            #
                            # Hello World
                            # =======

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
