EAD Toolbox
===========

31th January 2013 (2013-01-31)

Contents
--------

- `Description`_
- `Author(s)`_
- `Latest Version`_
- `Documentation`_
- `Requirements / Dependencies`_
- `Installation`_
- `Examples`_

  - `Command-line`_
  - `Web-based GUI`_
  - `Python API`_

- `Bugs, Feature requests etc.`_
- `Copyright & Licensing`_
                                   

Description
-----------

The EAD Toolbox provides a number of tools for working with `Encoded Archival 
Description`_ (EAD) XML documents.

Current capabilities include validation to the DTD, cross-walk to other 
metadata schemas, and extraction and display of subjects and named entities.

It also includes a web-based user interface for validating, cross-walking and
extracting data from your own EAD files, provided via a Python_ WSGI_ compliant
web application


Author(s)
---------

John Harrison <john.harrison@liv.ac.uk> at the `University of Liverpool`_ 


Latest Version
--------------

This is the first release of the software. There are no discrete version 
numbers as yet. Source code is under version control and available from:
http://github.com/bloomonkey/ead-toolbox


Documentation
-------------

At this time all documentation that exists can be found in this README file!


Requirements / Dependencies
---------------------------

- Python 2.6+
- lxml
- wsgiref >= 0.1.2 


Installation
------------

Users
~~~~~

``pip install git+http://github.com/bloomonkey/ead-toolbox.git#egg=eadtoolbox``


Developers
~~~~~~~~~~

I recommend that you use virtualenv_ to isolate your development environment
from system Python_ and any packages that may be installed there.

1. In GitHub_, fork the repository

2. Clone your fork:

    ``git clone git@github.com:<username>/ead-toolbox.git``

3. Install dependencies:

    ``pip install -r requirements.txt``

4. Install in develop / editable mode:

    ``pip install -e .``


Examples
--------

Command-line
~~~~~~~~~~~~

EAD Validation
''''''''''''''

To validate using the EAD 2002 DTD::

    ead-validate FILE

The EAD Toolbox currently only supports validation using the EAD 2002 DTD. I
hope to add validation using the XSD schema in the near future. 


Web-based GUI
~~~~~~~~~~~~~

The features availble though the commnad-line can also be accessed, and made
available to other users over a local network or the web, through the EAD
Sandbox application. Run the application using the following command::

    ead-sandbox [--hostname=HOSTNAME] [--port=PORT]


This will start a quick demonstration WSGI server (not recommended for
production use) to serve the application, and also open the application in a
new browser window/tab if possible. If you don't want the browser window/tab,
you can launch the application with the ``--no-browser`` option::

    ead-sandbox --no-browser [--hostname=HOSTNAME] [--port=PORT]


Python API
~~~~~~~~~~

EAD Validation
''''''''''''''

.. code-block:: python

    from lxml import etree
    from eadtoolbox.validate import EAD2002DTDValidator
    ead = etree.parse(open('eadfile.xml', 'r'))
    validator = EAD2002DTDValidator()
    if validator.validate(ead):
        print "VALID"
    else:
        print "INVALID"
        for e in validator.errors:
            print str(e)


Bugs, Feature requests etc.
---------------------------

Bug reports and feature requests can be submitted to the GitHub issue tracker:
http://github.com/bloomonkey/ead-toolbox/issues

If you'd like to contribute code, patches etc. please email the author, or
submit a pull request on GitHub.


Copyright & Licensing
---------------------

Copyright (c) University of Liverpool, 2010-2013

See LICENSE.rst for licensing details.


.. Links
.. _Python: http://www.python.org/
.. _WSGI: http://wsgi.org
.. _`Encoded Archival Description`: http://www.loc.gov/ead/
.. _`University of Liverpool`: http://www.liv.ac.uk
.. _GitHub: http://github.com
.. _virtualenv: http://www.virtualenv.org/en/latest/
