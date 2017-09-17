#!/usr/bin/env python

import io
import os
import re
from setuptools import setup, find_packages

file_dir = os.path.dirname(__file__)


def read(path, encoding='utf-8'):
    path = os.path.join(os.path.dirname(__file__), path)
    with io.open(path, encoding=encoding) as fp:
        return fp.read()


def version(path):
    """Obtain the packge version from a python file e.g. pkg/__init__.py
    See <https://packaging.python.org/en/latest/single_source_version.html>.
    """
    version_file = read(path)
    version_match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


LONG_DESCRIPTION = """
A project for handling csv files generated by PicoScope
"""

setup(
    name="braket-daq",
    version=version(os.path.join(file_dir, 'daq', '__init__.py')),
    author="Rob deCarvalho",
    author_email="unlisted@unlisted.net",
    description=("Picoscope file handling project"),
    license="BSD",
    keywords=("picoscope"),
    url="https://github.com/",
    packages=find_packages(),
    package_data={'daq': ['*.sh']},
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering',
    ],
    install_requires=[
        'hug',
        'gunicorn'
    ],
    entry_points={
        'console_scripts': [
            'daq.version = daq.commands:version.interface.cli',
            'daq.infect = daq.commands:infect.interface.cli',
            'daq.update = daq.commands:update.interface.cli',
            'daq.configure = daq.commands:configure.interface.cli',
            'daq.backup = daq.commands:backup.interface.cli',
        ],
    }
)
