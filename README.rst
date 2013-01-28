EAD Sandbox
===========

28th January 2013 (2013-01-28)

DEPRECATED: The EAD Sandbox has now been subsumed by the `EAD Toolbox`_


Contents
--------

 - `Description`_
 - `Author(s)`_
 - `Latest Version`_
 - `Requirements / Dependencies`_
 - `Documentation`_
 - `Bugs, Feature requests etc.`_
 - `File Manifest`_
 - `Copyright & Licensing`_
                                   

Description
-----------

The EAD Sandbox provides a Python_ WSGI_ compliant web application for playing
around with `Encoded Archival Description`_ (EAD) XML documents.

Current capabilities include validation to the DTD, cross-walk to other 
metadata schemas, and extraction and display of subject and named entities.


Author(s)
---------

John Harrison <john.harrison@liv.ac.uk> at the `University of Liverpool`_ 


Latest Version
--------------

This is the first release of the software. There are no discrete version 
numbers as yet. Source code is under version control and available from:
http://github.com/bloomonkey/ead-sandbox


Requirements / Dependencies
---------------------------

 - Python 2.6+
 - lxml
    

Documentation
-------------

At this time all documentation that exists can be found in this README file!

You can run an instance of the application by running the following command::

    python run.py [host [port]]


Bugs, Feature requests etc.
---------------------------

Bug reports and feature requests can be submitted to the GitHub issue tracker:
http://github.com/bloomonkey/ead-sandbox/issues

If you'd like to contribute code, patches etc. please email the author, or
submit a pull request on GitHub.


File Manifest
-------------
::

    css/
        eadsandbox.css
    html/
        head.tmpl
        home.html
        tail.tmpl
    xml/
        ead.dtd
        ead2isadg.xsl
        ead2marcxml.xsl
        ead2oai_dc.xsl
        ead2srw_dc.xsl
    README
    run.py


Copyright & Licensing
---------------------

Copyright (c) University of Liverpool, 2010-2013

This work is licensed under the Creative Commons 
Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of 
this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send 
a letter to Creative Commons, 171 Second Street, Suite 300, San Francisco, 
California, 94105, USA.


.. Links
.. _Python: http://www.python.org/
.. _WSGI: http://wsgi.org
.. _`Encoded Archival Description`: http://www.loc.gov/ead/
.. _`University of Liverpool`: http://www.liv.ac.uk
.. _`EAD Toolbox`: http://github.com/bloomonkey/ead-toolbox
