=============
pytest-sorter
=============

.. image:: http://img.shields.io/pypi/v/pytest-sorter.svg
    :target: https://pypi.python.org/pypi/pytest-sorter

.. image:: https://travis-ci.org/AndreMicheletti/pytest-sorter.svg?branch=master
    :target: https://travis-ci.org/AndreMicheletti/pytest-sorter
    :alt: See Build Status on Travis CI


A simple plugin to first execute tests that historically failed more

This `pytest`_ plugin was generated with `cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


Description
--------

This plugin will save a history of your tests executions in a file `.test_history`. For each test it will
have how many times it was executed, and how many times it failed.

Using that information it will calculate the percentage of failure of tests, and order them
to first execute the higher *failure ratio*

Requirements
------------

* Python>=3

Installation
------------

You can install "pytest-sorter" via `pip`_ from `PyPI`_::

    $ pip install pytest-sorter


Usage
-----

After installed, your tests will automatically create and update the `.test_history` file,
and order tests by their failure ratio.

You can tell pytest to ignore this plugin by passing:
```
pytest --no-sorted
```

Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-sorter" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/AndreMicheletti/pytest-sorter/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.python.org/pypi/pip/
.. _`PyPI`: https://pypi.python.org/pypi
