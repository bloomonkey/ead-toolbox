EAD Toolbox
===========

28th January 2013 (2013-01-28)

Contents
--------

 - `Description`_
 - `Author(s)`_
 - `Latest Version`_
 - `Requirements / Dependencies`_
 - `Documentation`_
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


Requirements / Dependencies
---------------------------

 - Python 2.6+
 - lxml
    

Documentation
-------------

At this time all documentation that exists can be found in this README file!

You can run the application by running the following command::

    ead-sandbox [--hostname=HOSTNAME] [--port=PORT]


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
