"""Validate EAD Documents"""

from __future__ import with_statement

import sys
import os.path
import logging

from lxml import etree
from pkg_resources import resource_stream
from argparse import ArgumentParser


class EADValidator(object):
    "Abstract Base Class object for validating EAD instances"
    
    def validate(self, ead):
        "Validate the parsed ElementTree in ``ead``, return True or False."
        raise NotImplementedError


class EAD2002DTDValidator(EADValidator):
    "Validation according to the EAD 2002 DTD."
    
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
    

def validate(argv=None):
    global argparser
    if argv is None:
        args = argparser.parse_args()
    else:
        args = argparser.parse_args(argv)
    for filepath in args.file:
        # Check for well-formedness by attempting to parse the file
        try:
            with open(filepath) as fh:
                try:
                    ead = etree.parse(fh)
                except etree.XMLSyntaxError as e:
                    logging.error("Not well-formed XML: %s",
                                  e)
                    return 1
        except IOError as e:
            # Log non existent file
            logging.error("%s: %s", str(e.args[1]), filepath)
            # Skip to next file
            continue
        if not any([args.dtd, args.xsd]):
            # Try to guess which type of validation to carry out
            # Default to DTD validation
            args.dtd = True
        
        if args.xsd:
            # TODO: add validation using the XSD schema
            msg = ("Validation to XSD Schema is not yet available; "
                   "coming soon...")
            logging.error(msg)
            raise NotImplementedError(msg)
        elif args.dtd:
            validator = EAD2002DTDValidator()
        if validator.validate(ead):
            logging.info("SUCCESS! %s PASSED %s",
                         filepath,
                         validator.__class__.__doc__)
        else:
            logging.error('\n'.join([str(e) for e in validator.errors]))
            return 2
    return 0


# Configure logger
logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s',
                    level=logging.DEBUG)

# Set up argument parser
argparser = ArgumentParser(description=__doc__.splitlines()[0])
# Positional argument for filename(s)
argparser.add_argument('file',
                       action='store',
                       nargs='+',
                       help="file(s) to validate"
                       )

group = argparser.add_mutually_exclusive_group()
group.add_argument('-d', '--dtd',
                   action='store_true', dest='dtd',
                   default=False,
                   help="validate using the DTD (EAD 2002)")
group.add_argument('-x', '--xsd',
                   action='store_true', dest='xsd',
                   default=False,
                   help="validate using the XSD XML Schema (EAD 2002)")


if __name__ == "__main__":
    sys.exit(validate())