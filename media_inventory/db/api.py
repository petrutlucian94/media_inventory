import logging
import urllib2
from urlparse import urljoin

LOG = logging.getLogger('media_inventory')


class DBAPI(object):
    # _DEFAULT_DB_URL = 'http://127.0.0.1:8080/basex/rest/test'
    _DEFAULT_DB_URL = 'http://127.0.0.1:8080/basex/rest/media_inventory_test'

    def __init__(self, db_url=None):
        db_url = db_url or self._DEFAULT_DB_URL

    def _db_request(self, url='', method='GET', data=None, expand_url=True,
                    content_type='application/xml'):
        opener = urllib2.build_opener()

        if expand_url:
            url = urljoin(self._DEFAULT_DB_URL, url)

        req = urllib2.Request(url, data=data)
        req.add_header('Content-Type', content_type)
        req.get_method = lambda: method

        try:
            LOG.debug('DB Request: %(method)s - %(url)s - '
                      'Content Type %(content_type)s '
                      '- Request body: %(data)s' % locals())

            response = opener.open(req)
            response_body = response.read()

            LOG.debug('DB response: %(response_body)s' % locals())
            return response_body
        except urllib2.HTTPError as e:
            LOG.error('DBError: %s - %s' % (e.code, e.read()))
            raise

    def _get_basex_query(self, xquery):
        query = '''
            <query xmlns="http://basex.org/rest">
            <text><![CDATA[%s]]></text>
            </query>''' % xquery
        return query

    def query(self, xquery=None):
        basex_query = self._get_basex_query(xquery)
        result = self._db_request(method='POST', data=basex_query)
        return result

    def insert(self, node, location):
        xquery = '''
            let $node := %(node)s
            return
            insert node $node as last into %(location)s
        ''' % dict(node=node, location=location)

        self.query(xquery)

    def create_db(self):
        self._db_request(method='PUT', data='<inventory></inventory>')

    def ensure_db_exists(self):
        try:
            self._db_request()
        except urllib2.HTTPError as e:
            if e.code == 404:
                self.create_db()
            else:
                raise
