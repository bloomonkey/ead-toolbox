"""Transform EAD Documents"""

from __future__ import with_statement

import os.path

from lxml import etree
from pkg_resources import resource_stream


class EadTransformer(object):
    "Abstract Base Class object for transforming EAD documents."
    
    def transform(self, ead):
        "Transform the ``ead``."
        raise NotImplementedError


class XsltEadTransformer(EadTransformer):
    "Abstract Base Class object for transforming XML using XSLT."
    
    def __init__(self, xslt):
        try:
            # Parse the XSLT from a file-like object
            xslt = etree.parse(xslt)
        except IOError:
            # xslt arg was raw XSLT string/unicode?
            try:
                xslt = etree.fromstring(xslt)
            except:
                # path to XSLT file?
                if os.path.isfile(xslt):
                    with open(xslt, 'r') as fh:
                        xslt = etree.parse(fh)
                else:
                    raise ValueError("While constructing {0.__class__.__name__}"
                                     ", `xslt` is not one of:\n"
                                     "* file-like object\n"
                                     "* path to an XSLT file\n"
                                     "* raw XSLT string / unicode\n"
                                     "".format(self))
        self._txr = etree.XSLT(xslt)

    def transform(self, ead):
        return self._txr(ead)
        
    def transform_to_unicode(self, ead):
        out = self.transform(ead)
        return etree.tostring(out)


if __name__ == '__main__':
    pass