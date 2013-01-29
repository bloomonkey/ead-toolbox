"""Validate EAD Documents"""

from __future__ import with_statement

from lxml import etree
from pkg_resources import resource_stream


class EADValidator(object):
    "Abstract Base Class object for validating EAD instances"
    
    def validate(self, ead):
        "Validate the parsed ElementTree in ``ead``, return True or False."
        raise NotImplementedError


class EAD2002DTDValidator(EADValidator):
    "Validator to validate using the EAD 2002 DTD."
    
    def __init__(self):
        with resource_stream('eadtoolbox', 'data/xml/ead.dtd') as fh:
            self._dtd = etree.DTD(fh)

    @property
    def dtd(self):
        "Get the DTD."
        return self._dtd

    @property
    def errors(self):
        "Get any errors that occurred while validating"
        return self.dtd.error_log.filter_from_errors()
    
    def validate(self, ead):
        return self.dtd.validate(ead)
    

if __name__ == '__main__':
    pass