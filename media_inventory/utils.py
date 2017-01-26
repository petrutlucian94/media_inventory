import uuid
import logging
import os
from StringIO import StringIO

from lxml import etree

import media_inventory

LOG = logging.getLogger('media_inventory')

_schema_cache = {}


def get_abs_path(path):
    # Accepts paths relative to the project location
    # and returns an absolute path.
    base_path = os.path.abspath(os.path.dirname(media_inventory.__file__))
    return os.path.join(base_path, path)


def _get_schema(schema_path):
    schema = _schema_cache.get(schema_path)
    if schema:
        return schema

    LOG.debug("Loading XML schema %s" % schema_path)
    try:
        with open(schema_path, 'r') as f:
            schema_content = f.read()

        schema_doc = etree.parse(StringIO(schema_content))
        schema = etree.XMLSchema(schema_doc)
    except Exception:
        LOG.exception("Failed to load XML schema: %s")
        raise

    _schema_cache[schema_path] = schema
    return schema


def validate_schema(str_xml, schema_path):
    schema = _get_schema(schema_path)
    schema.assertValid(etree.parse(StringIO(str_xml)))


def generate_uuid(dashed=True):
    if dashed:
        return str(uuid.uuid4())
    return uuid.uuid4().hex


def _format_uuid_string(string):
    return (string.replace('urn:', '')
                  .replace('uuid:', '')
                  .strip('{}')
                  .replace('-', '')
                  .lower())


def is_uuid_like(val):
    try:
        return str(uuid.UUID(val)).replace('-', '') == _format_uuid_string(val)
    except (TypeError, ValueError, AttributeError):
        return False
