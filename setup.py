#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-sorter',
    version='0.2.0',
    author='Andre Luiz Micheletti',
    author_email='andreluizmtmicheletti@gmail.com',
    maintainer='Andre Luiz Micheletti',
    maintainer_email='andreluizmtmicheletti@gmail.com',
    license='MIT',
    url='https://github.com/AndreMicheletti/pytest-sorter',
    description='A simple plugin to first' +
    ' execute tests that historically failed more',
    long_description=read('README.rst'),
    package_dir={'': 'tests'},
    packages=[''],
    python_requires='>=3.6',
    install_requires=['pytest>=3.1.1'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'sorter = pytest_sorter',
        ],
    },
)
