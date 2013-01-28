"""
Created on Nov 4, 2010

@author: John Harrison <johnpaulharrison@gmail.com>
"""

import cgi
import os
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from lxml import etree

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
        with open(os.path.join('html', 'head.tmpl'), 'r') as fh:
            return fh.readlines()
        
    def _tail(self):
        # Return HTML Tail
        with open(os.path.join('html', 'tail.tmpl'), 'r') as fh:
            return fh.readlines()
        
    def _apply_xslt(self, tree, xslt_path):
        # Apply XSLT from xslt_path to tree and return result as an lxml tree
        try:
            txr = self.txrs[xslt_path]
        except KeyError:
            with open(xslt_path, 'r') as fh:
                xslt = etree.parse(fh)
            self.txrs[xslt_path] = txr = etree.XSLT(xslt)
        return txr(tree)
    
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
            with open(os.path.join('html', 'home.html'), 'r') as fh:
                out.extend(fh.readlines())
            out.extend(self._tail())
            
        elif path.startswith('css/'):
            # Return static CSS
            self.response_headers.append(('Content-Type', 'text/css'))
            with open(os.path.join(*path.split('/')), 'r') as fh:
                out.extend(fh.readlines())
                
        elif path == "play":
            form = cgi.FieldStorage(fp=environ['wsgi.input'], 
                                    environ=environ)
            xml = self._fetch_ead(form)
            try:
                ead = etree.fromstring(xml)
            except etree.XMLSyntaxError:
                # make use of browser default XML errors
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
                    with open(os.path.join('xml', 'ead.dtd'), 'r') as fh:
                        dtd = etree.DTD(fh)
                    if dtd.validate(ead):
                        out.append('<h2>Validation Passed!</h2>')
                    else:
                        out.append('<h2>Validation Failed!</h2>')
                        out.extend(['<p>{0}</p>'.format(e) for e in dtd.error_log.filter_from_errors()])
                    out.extend(self._tail())
                    
                elif func == "to isad(g)":
                    out.extend(self._head())
                    out.append('<h2>ISAD(G)</h2>')
                    xslt_path = os.path.join('xml', 'ead2isadg.xsl')
                    result = self._apply_xslt(ead, xslt_path)
                    out.append(etree.tostring(result))
                    out.extend(self._tail())
                    
                elif func == "to dc":
                    xslt_path = os.path.join('xml', 'ead2oai_dc.xsl')
                    result = self._apply_xslt(ead, xslt_path)
                    # Sacrifice potentially pretty XML display for browser compatibility
                    self.response_headers.append(('Content-Type', 'text/plain; charset=UTF-8"'))
                    out.append(etree.tostring(result, pretty_print=True, encoding='utf-8'))
                    
                elif func == "to marc":
                    xslt_path = os.path.join('xml', 'ead2marcxml.xsl')
                    result = self._apply_xslt(ead, xslt_path)
                    # Sacrifice potentially pretty XML display for browser compatibility
                    self.response_headers.append(('Content-Type', 'text/plain; charset=UTF-8"'))
                    out.append(etree.tostring(result, pretty_print=True, encoding='utf-8'))
                    
                elif func == 'xsl-fo':
                    xslt_path = os.path.join('xml', 'ead2fo.xsl')
                    result = self._apply_xslt(ead, xslt_path)
                    self.response_headers.append(('Content-Type', 'application/xml'))
                    out.append(etree.tostring(result, pretty_print=True, encoding='utf-8'))
                    
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
        