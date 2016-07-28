# Load in our dependencies
import os
from setuptools import setup, find_packages

# Load in VERSION from standalone file to avoid loading library
with open(os.path.join(os.path.dirname(__file__), 'restructuredtext_lint', 'VERSION'), 'r') as version_file:
    VERSION = version_file.read().strip()

# Declare our library
setup(
    name='restructuredtext_lint',
    version=VERSION,
    description='reStructuredText linter',
    long_description=open('README.rst').read(),
    keywords=[
        'restructuredtext',
        'restructured text',
        'rest',
        'rst',
        'lint'
    ],
    author='Todd Wolfson',
    author_email='todd@twolfson.com',
    url='https://github.com/twolfson/restructuredtext-lint',
    download_url='https://github.com/twolfson/restructuredtext-lint/archive/master.zip',
    entry_points={
        'console_scripts': [
            'restructuredtext-lint = restructuredtext_lint.cli:main',
            'rst-lint = restructuredtext_lint.cli:main'
        ]
    },
    packages=find_packages(),
    license='UNLICENSE',
    install_requires=open('requirements.txt').readlines(),
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Topic :: Text Processing :: Markup'
    ]
)
