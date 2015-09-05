========
Overview
========

haralyzer-api is a deployable REST API wrapper for the haralyzer package. It provides
simple functionality for storing raw HAR data and analyzing the contents. The primary
purpose is to provide an easy way to search for page statistics by hostname, URI, date of
the run, etc.

=========================
Terminology And Structure
=========================

The API uses two main data structures that represent those of a HAR file. Please
review the API endpoint documentation for a full breakdown of the fields provided
by these resources.

`Endpoints <endpoints.html>`_

----
Test
----

This represents a single "test" run converted to a HAR file. It represents a full
browser session in the sense that it can contain multiple pages.

----
Page
----

A single page from a given HAR test. This is where the important data lives, such as
the overall performance data.

------------
Sample Usage
------------

.. code-block:: python

    import requests

    with open('my/har_data.har', r') as f:
        payload = {'har_data': f.read()}
        r = responses.post(API_URL, data=payload)
        print r.text

    # output would be:
    {
    "data": {
        "browser_name": "Firefox", 
        "browser_version": "25.0.1", 
        "hostname": "humanssuck.net", 
        "id": 1, 
        "name": null, 
        "pages": [
            {
                "audio_load_time": 0.0, 
                "audio_size": 0.0, 
                "css_load_time": 76.0, 
                "css_size": 8.0, 
    .....................................

Again, please consult the endpoint documentation for details on resources:

`Endpoints <endpoints.html>`_
