import logging

from lxml import etree
from StringIO import StringIO

from media_inventory import utils

LOG = logging.getLogger('media_inventory')


class BaseModel(object):
    _schema = None

    def __init__(self, str_xml):
        parser = etree.XMLParser(schema=self._schema)

        self._xml = etree.parse(StringIO(str_xml), parser)
        self._root = self._xml.getroot()

        if not self.id:
            LOG.debug("Did not find a movie id. Generating one.")
            self._root.set('id', utils.generate_uuid())
        elif not utils.is_uuid_like(self.id):
            raise Exception(
                "Got id %s which does not look like an UUID." % self.id)

    @property
    def id(self):
        return self._root.get('id')

    def to_xml(self):
        return etree.tostring(self._root)
