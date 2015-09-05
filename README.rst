=============
haralyzer-api
=============

.. image:: https://travis-ci.org/mrname/haralyzer-api.svg?branch=master
    :target: https://travis-ci.org/mrname/haralyzer-api

.. image:: https://coveralls.io/repos/mrname/haralyzer-api/badge.svg?branch=master
  :target: https://coveralls.io/r/mrname/haralyzer-api?branch=master

.. image:: https://readthedocs.org/projects/haralyzer-api/badge/?version=latest
    :target: http://haralyzer-api.readthedocs.org/en/latest/

A REST API For Har Data Analysis

Overview
--------

The haralyzer API module provides a deployable REST API for storing raw HAR
data and extracting performance data for the pages inside the HAR data.

Status
------

This is currently SUPER beta, with limited features, and no guarantees as to appropriate
functionality.

Development Process
-------------------

Start by forking the repository, and cloning down your fork. Make a fresh virtualenv,
and then install the developer requirements.

    pip install -r developer_requirements

    python setup.py develop

Run the tests:

    py.test tests/

IMPORTANT: This application REQUIRES Redis. I have been too lazy to use any kind of mocking or
db fixtures, so you need to have Redis running locally for the tests to complete. SORRY!

The repo has Travis CI and Coveralls integration, so please do the needful with repo
access on your account.

PLEASE write tests for your new code! Travis and Coveralls makes it easy to see if you
are missing coverage on any of your new stuff.

When you are finished, just open a pull request!

Schema Changes
--------------

This project uses flask-migrate to manage schema changes. Consult the docs_ if you have
questions about how to use it.

.. _docs: http://flask-migrate.readthedocs.org/en/latest/

Project Documentation
---------------------

.. _Haralyzer API Documentation: http://haralyzer-api.readthedocs.org/
