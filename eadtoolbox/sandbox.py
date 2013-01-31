"""EAD Sandbox WSGI Application.

The EAD Sandbox provides a Python WSGI compliant web application for playing
around with Encoded Archival Description (EAD) XML documents.

Current capabilities include validation to the DTD, cross-walk to other
metadata schemas, and extraction and display of subject and named entities.
"""

import cgi
import socket
import sys
import webbrowser
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from lxml import etree
from pkg_resources import resource_stream, resource_string
from argparse import ArgumentParser
from wsgiref.simple_server import make_server


from eadtoolbox.validate import EAD2002DTDValidator
from eadtoolbox.transform import XsltEadTransformer


class EADSandboxWsgiApp(object):
    """EAD Sandbox WSGI Application."""

    def __init__(self):
        self.response_headers = []
        self.txrs = {}
        
    def _fetch_ead(self, form):
        # Fetch EAD XML from the submitted form
        xml = form['eadfile'].value
        if not xml:
            xml = form.getfirst('eadxml')
        return xml
    
    def _head(self):
        # Return HTML Head
        self.response_headers.append(('Content-Type', 'text/html'))
        return [resource_string('eadtoolbox', 'data/html/head.tmpl')]
        
    def _tail(self):
        # Return HTML Tail
        return [resource_string('eadtoolbox', 'data/html/tail.tmpl')]
        
    def _apply_xslt(self, tree, xslt_path):
        # Apply XSLT from xslt_path to tree and return result as an lxml tree
        try:
            transformer = self.txrs[xslt_path]
        except KeyError:
            fh = resource_stream('eadtoolbox', 'data/xml/{0}'.format(xslt_path))
            self.txrs[xslt_path] = transformer = XsltEadTransformer(fh)
            
        return transformer.transform(tree)
    
    def _html_listItems_from_xpath(self, ead, xpath):
        # Return HTML list items from elements in ead that match XPath
        matches = ead.xpath(xpath)
        for xp in matches:
            xml_str = etree.tostring(xp, method="text", encoding="utf-8")
            yield '<li>{0}</li>'.format(xml_str.strip())
                
    def __call__(self, environ, start_response):
        # Method to make instances of this class callable
        self.environ = environ
        path = environ.get('PATH_INFO', '').strip('/')
        self.response_headers = []
        out = []
        if not len(path):
            # Return homepage
            out.extend(self._head())
            out.append(resource_string('eadtoolbox', 'data/html/home.html'))
            out.extend(self._tail())
            
        elif path.startswith('css/'):
            # Return static CSS
            self.response_headers.append(('Content-Type', 'text/css'))
            out.append(resource_string('eadtoolbox', 'data/{0}'.format(path)))
                
        elif path == "play":
            form = cgi.FieldStorage(fp=environ['wsgi.input'], 
                                    environ=environ)
            xml = self._fetch_ead(form)
            try:
                ead = etree.fromstring(xml)
            except etree.XMLSyntaxError:
                # Make use of browser default XML errors
                self.response_headers.append(('Content-Type', 'application/xml'))
                out.append(xml)
            else:
                func = form.getfirst('submit').lower()
                
                if func == 'show':
                    # Sacrifice potentially pretty XML display for browser compatibility
                    self.response_headers.append(('Content-Type', 'text/plain; charset=UTF-8"'))
                    xml_str = etree.tostring(ead, pretty_print=True, encoding='utf-8')
                    out.append(xml_str)
                    
                elif func == "validate":
                    out.extend(self._head())
                    validator = EAD2002DTDValidator()
                    
                    if validator.validate(ead):
                        out.append('<h2>Validation Passed!</h2>')
                    else:
                        out.append('<h2>Validation Failed!</h2>')
                        out.extend(['<p>{0}</p>'.format(e) for e in validator.errors])
                    out.extend(self._tail())
                    
                elif func == "to isad(g)":
                    out.extend(self._head())
                    out.append('<h2>ISAD(G)</h2>')
                    xslt_path = 'ead2isadg.xsl'
                    result = self._apply_xslt(ead, xslt_path)
                    out.append(etree.tostring(result, encoding='utf-8'))
                    out.extend(self._tail())
                    
                elif func == "to dc":
                    xslt_path = 'ead2oai_dc.xsl'
                    result = self._apply_xslt(ead, xslt_path)
                    # Sacrifice potentially pretty XML display for browser compatibility
                    self.response_headers.append(('Content-Type',
                                                  'text/plain; charset=UTF-8"'))
                    out.append(etree.tostring(result,
                                              pretty_print=True,
                                              encoding='utf-8')
                    )
                elif func == "to marc":
                    xslt_path = 'ead2marcxml.xsl'
                    result = self._apply_xslt(ead, xslt_path)
                    # Sacrifice potentially pretty XML display for browser compatibility
                    self.response_headers.append(('Content-Type',
                                                  'text/plain; charset=UTF-8"'))
                    out.append(etree.tostring(result,
                                              pretty_print=True,
                                              encoding='utf-8')
                    )
                    
                elif func == 'people':
                    out.extend(self._head())
                    out.extend(['<h2>{0}</h2>'.format(func.title()),
                                '<ul>'
                                ])
                    out.extend(self._html_listItems_from_xpath(ead, '//persname'))
                    out.extend(self._html_listItems_from_xpath(ead, '//famname'))
                    out.append('</ul>')
                    out.extend(self._tail())
                    
                elif func == 'places':
                    out.extend(self._head())
                    out.extend(['<h2>{0}</h2>'.format(func.title()),
                                '<ul>'
                                ])
                    out.extend(self._html_listItems_from_xpath(ead, '//geogname'))
                    out.append('</ul>')
                    out.extend(self._tail())
                    
                elif func == 'subjects':
                    out.extend(self._head())
                    out.extend(['<h2>{0}</h2>'.format(func.title()),
                                '<ul>'
                                ])
                    out.extend(self._html_listItems_from_xpath(ead, '//subject'))
                    out.append('</ul>')
                    out.extend(self._tail())
                    
        else:
            self.response_headers.append(('Content-Type', 'text/plain'))
            out = ["Unsupported Operation"]
        self.response_headers.append(('Content-Length', str(sum([len(d) for d in out]))))
        start_response("200 OK", self.response_headers)
        return out


def start(argv=None):
    global argparser, application
    if argv is None:
        args = argparser.parse_args()
    else:
        args = argparser.parse_args(argv)
    
    httpd = make_server(args.hostname, args.port, application)
    url = "http://{0}:{1}".format(args.hostname, args.port)
    if args.browser:
        webbrowser.open(url)
        print ("Hopefully a new browser window/tab should have opened "
               "displaying the application.")
        print "If not, you should be able to access the application at:"
    else:
        print "You should be able to access the application at:"
        
    print url
    return httpd.serve_forever()


# Create an instance of the application
application = EADSandboxWsgiApp()

# Set up argument parser
argparser = ArgumentParser(description=__doc__.splitlines()[0])
# Find default hostname
try:
    hostname = socket.gethostname()
except:
    hostname = 'localhost'

argparser.add_argument('--hostname', type=str,
                       action='store', dest='hostname',
                       default=hostname, metavar='HOSTNAME',
                       help=("name of host to listen on. default derived by "
                             "inspection of local system"))
argparser.add_argument('-p', '--port', type=int,
                       action='store', dest='port',
                       default=8008, metavar='PORT',
                       help="number of port to listen on. default: 8008")
argparser.add_argument('--no-browser',
                       action='store_false', dest='browser',
                       default=True,
                       help=("don't open a browser window/tab containing the "
                             "app. useful if you want to deploy the app for "
                             "other users"
                             )
                       )


if __name__ == "__main__":
    sys.exit(start())
