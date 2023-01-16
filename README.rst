Introduction
============


.. image:: https://readthedocs.org/projects/circuitpython-async-button/badge/?version=latest
    :target: https://circuitpython-async-button.readthedocs.io/
    :alt: Documentation Status



.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/furbrain/CircuitPython_async_button/workflows/Build%20CI/badge.svg
    :target: https://github.com/furbrain/CircuitPython_async_button/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

This library provides an asynchronous way to wait for buttons to be pressed. It also provides
detection of single, double and triple clicks, and also long presses.



Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `CircuitPython asyncio module <https://github.com/adafruit/Adafruit_CircuitPython_asyncio>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython-async-button/>`_.
To install for current user:

.. code-block:: shell

    pip3 install circuitpython-async-button

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-async-button

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .env/bin/activate
    pip3 install circuitpython-async-button

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install async_button

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage
=====

There are two classes:

* ``SimpleButton``: This allows to ``await`` for presses and releases

  .. code-block:: python

     button = async_button.SimpleButton(board.D5, True)
     await button.pressed

* ``Button``: This has much more features. It creates a background process to monitor the button
  and allows the user to ``await`` for single clicks, double clicks, long clicks etc. It must be instantiated
  in an asynchronous environment

  .. code-block:: python

     button = async_button.Button(board.D5, True)
     click = await button.wait_for_click()
     if click == button.DOUBLE:
         print("Double click!")

See the examples folder for full demonstrations

Documentation
=============
API documentation for this library can be found on `Read the Docs <https://circuitpython-async-button.readthedocs.io/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/furbrain/CircuitPython_async_button/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
