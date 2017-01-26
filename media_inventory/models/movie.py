import os

from media_inventory.models import base as base_model
from media_inventory import utils


class Movie(base_model.BaseModel):
    def __init__(self, *args, **kwargs):
        schema_location = utils.get_abs_path(
            os.path.join('api', 'schema', 'movie.xsd'))
        self._schema = utils.get_schema(schema_location)

        super(Movie, self).__init__(*args, **kwargs)
