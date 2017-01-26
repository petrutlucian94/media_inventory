import logging
import os

from flask import request

from media_inventory.db import api as db_api
from media_inventory import utils

LOG = logging.getLogger('media_inventory')


class BaseAPIController(object):
    def __init__(self, flask_app):
        self._app = flask_app
        self._db_api = db_api.DBAPI()

    def _get_xml_schema_path(self, name):
        rel_path = os.path.join('api', 'schema', '%s.xsd' % name)
        schema_path = utils.get_abs_path(rel_path)
        return schema_path

    def validate_request(self, schema_name):
        schema_path = self._get_xml_schema_path(schema_name)
        request_data = request.get_data()

        utils.validate_schema(request_data, schema_path)

    def setup(self):
        pass
