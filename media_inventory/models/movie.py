import os

from media_inventory.models import base as base_model
from media_inventory import utils


class Movie(base_model.BaseModel):
    _schema_location = utils.get_abs_path(
        os.path.join('api', 'schema', 'movie.xsd'))
