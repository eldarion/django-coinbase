===============
django-coinbase
===============

a Django app for receiving payment notifications from Coinbase


.. image:: https://img.shields.io/travis/eldarion/django-coinbase.svg
    :target: https://travis-ci.org/eldarion/django-coinbase

.. image:: https://img.shields.io/coveralls/eldarion/django-coinbase.svg
    :target: https://coveralls.io/r/eldarion/django-coinbase

.. image:: https://img.shields.io/pypi/dm/django-coinbase.svg
    :target:  https://pypi.python.org/pypi/django-coinbase/

.. image:: https://img.shields.io/pypi/v/django-coinbase.svg
    :target:  https://pypi.python.org/pypi/django-coinbase/

.. image:: https://img.shields.io/badge/license-BSD-blue.svg
    :target:  https://pypi.python.org/pypi/django-coinbase/


Getting Started
---------------

This is a fairly simple app. It's three parts:

1. Webhook View
2. Model to store the webhook received data
3. Signal emitted on reciept/validation/storage of webhook data

First off, you'll want to add `django-coinbase` to your requirements.txt and
pip install it in your virtualenv. Next you'll want to add `coinbase` to your
`INSTALLED_APPS` setting of your `settings.py` file. Lastly, you'll want to
add a urls include to your main `urls.py` file for `coinbase.urls`.

There is a signal that you can setup a receiver for in your own project to do
something with the callback data::

    @receiver(order_received)
    def handle_order_received(sender, order, **kwargs):
        pass  # do something with the order object, like enable a feature based on order.custom contents

You will want to set two different settings:

COINBASE_API_KEY
^^^^^^^^^^^^^^^^

This is the API Key found at: https://coinbase.com/account/integrations


COINBASE_SHARED_SECRET
^^^^^^^^^^^^^^^^^^^^^^

This is just a random key you make up and store in your settings and add to the
querystring of the Instant Payment Notifications field (https://coinbase.com/merchant_settings).

This is the URL of your site + wherever you rooted the urls include + `/cb/`
followed with the querystring parameter `secret` followed by the value of this
settings.

For example::

    # urls.py
    url(r"^payments/", include("coinbase.urls"))
    
    # settings.py
    COINBASE_SHARED_SECRET = "mysecretsauce"
    
    >>> Site.objects.get_current().domain
    example.com
    
    # Your url would be
    http://example.com/payments/cb/?secret=mysecretsauce



Development
-----------

To run test suite::

    $ pip install Django django-nose django-jsonfield mock requests
    $ python runtests.py


Commercial Support
------------------

This app, and many others like it, have been built in support of many of Eldarion's
own sites, and sites of our clients. We would love to help you on your next project
so get in touch by dropping us a note at info@eldarion.com.
