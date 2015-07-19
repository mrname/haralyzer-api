#!/usr/bin/env python
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

install_requires = [
    "Flask",
    "Flask-Migrate",
    "Flask-RESTful",
    "Flask-SQLAlchemy",
    "haralyzer",
]


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='haralyzer-api',
    version='0.0.1',
    description='REST API for storing HAR data and retrieving analyzed results',
    author='Justin Crown',
    author_email='admin@humanssuck.net',
    url='https://github.com/mrname/haralyzer-api',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Eve',
        'License :: MIT',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    license='MIT',
    # Needed for the mock adapter
    zip_safe=False,
)
