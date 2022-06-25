.. runtime-final documentation master file, created by
   sphinx-quickstart on Sat Jun 25 01:52:43 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. currentmodule:: runtime_final
   
Welcome to runtime-final's documentation!
=========================================

``runtime-final`` is a simple module that allows you declare final classes
and methods that are validated at runtime.

This module is inspired by and is fully compatible with :func:`typing.final` decorator.
See `PEP-591 <https://www.python.org/dev/peps/pep-0591>`_ for more details about this topic.
The compatiblity is described in documentation of :func:`final` decorator.

Installation
------------

This module is hosted on PyPi and can easily be installed with::

   $ python -m pip install runtime-final


Usage
-----

For usage examples, See documentation of :func:`final` decorator.

Reference
---------

Following are all the components that are provided by this module.

Metadata
~~~~~~~~

.. data:: __version__

   The current version of the module.

.. data:: __author__
   
   The author of the package.

.. data:: __copyright__
   
   The copyright notice for this module.


``@final`` decorator
~~~~~~~~~~~~~~~~~~~~

.. autofunction:: final

Helpers
~~~~~~~

.. autofunction:: is_final
.. autofunction:: get_final_methods
