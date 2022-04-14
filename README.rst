openstack_loadtest
==================

.. image:: https://github.com/hemna/openstack-loadtest/workflows/python/badge.svg
    :target: https://github.com/hemna/openstack-loadtest/actions

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://black.readthedocs.io/en/stable/

.. image:: https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
    :target: https://timothycrosley.github.io/isort/

Python project that uses the Python Locust library to create load tests for
OpenStack services.

Requirements
------------

Python 3.6+.

.. note::

    Because `Python 2.7 supports ended January 1, 2020 <https://pythonclock.org/>`_, new projects
    should consider supporting Python 3 only, which is simpler than trying to support both.
    As a result, support for Python 2.7 in this example project has been dropped.

Dependencies
------------

Dependencies are defined in:

- ``requirements.in``

- ``requirements.txt``

- ``dev-requirements.in``

- ``dev-requirements.txt``


Usage
-----


First install the project with pip

* git clone https://github.com/hemna/openstack-loadtest
* cd openstack-loadtest
* virtualenv .venv
  (make sure you are using python3 binary for virtualenv)
* source .venv/bin/activate
* pip install .


Make sure you have a ~/.config/openstack/clouds.yaml configured to point
to your openstack deployment.

Then set the OS_CLOUD env var to use an entry in your ~/.config/openstack/clouds.yaml

* export OS_CLOUD=devstack

Run the load test for fetching the cinder volumes detail test

*  locust -f src/openstack_loadtest/cinder.py CinderUser --headless --tags volumes_info -u10 -t 30s


locust -f src/openstack_loadtest/barbican.py BarbicanUser --headless --tags secret_info -u5 -t 60s
locust -f src/openstack_loadtest/glance.py GlanceUser --headless --tags images_info -u5 -t 60s
