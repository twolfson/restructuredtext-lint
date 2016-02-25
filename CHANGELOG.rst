restructuredtext-lint changelog
===============================
0.14.2 - Documented common PyPI issues

0.14.1 - Fixed up indentation annoyances in README

0.14.0 - Repaired JSON with no errors via @Iyozhikov in #25

0.13.0 - Added absolute imports to repair local development

0.12.4 - Added CPython@3.4, CPython@3.5, and PyPy@3 to Travis CI tests

0.12.3 - Added `foundry` for release

0.12.2 - Repaired imports to be absolute within package to fix Python3 issues via @fizyk in #21

0.12.1 - Added ``flake8-quotes`` to lint for non-single quotes

0.12.0 - Added support for multiple ``.rst`` files to ``rst-lint`` command via @pwilczynskiclearcode in #19

0.11.3 - Documented added in new directives/roles

0.11.2 - Added test failures for lint errors

0.11.1 - Fixed bad assertions in tests

0.11.0 - Added fix for errors that have no line number (e.g. invalid links). Fixes #12

0.10.0 - Remerged change from ``0.8.0`` to loosen ``docutils`` dependency to allow minor fluctuations. Fixes #9

0.9.0 - Added ``flake8`` linting via @berendt in #10

0.8.0 - Loosened ``docutils`` dependency to allow minor fluctuations. Fixes #9

0.7.0 - Increased ``halt_level`` to 5 (never halt) to collect all errors. Fixes #7

0.6.0 - Rewrote library to be inline with ``rst2html.py`` flow. Added error collecting on transforms. Fixes #6

0.5.0 - Relocated tests to follow convention and make running specific tests easier

0.4.0 - Repaired regression for bad parses that did not return all promised data (e.g. line number). Fixes #5

0.3.1 - Documented ``lint_file`` method

0.3.0 - Moved from ``read`` to ``io.read``, allowing specification of ``encoding`` from CLI. Attribution to @coldfix

0.2.0 - Added CLI utility

0.1.1 - Repairing link for PyPI

0.1.0 - Initial release
