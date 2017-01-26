import logging

from flask import Flask

from media_inventory.db import api as db_api
from media_inventory.api.controllers import movies

app = Flask('media_inventory')
LOG = app.logger


class MediaInventoryAPI(object):
    # For now, we'll just hardcode stuff..
    _api_controllers = [movies.MoviesController]

    def setup(self):
        self.setup_logging()
        self.setup_db()
        self.setup_controllers()

        app.run()

    def setup_logging(self):
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)

        log_fmt = '[%(asctime)s] %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_fmt)
        handler.setFormatter(formatter)

        LOG.addHandler(handler)
        LOG.setLevel(logging.DEBUG)

    def setup_db(self):
        self._db_api = db_api.DBAPI()
        self._db_api.ensure_db_exists()

    def setup_controllers(self):
        for api_controller in self._api_controllers:
            api_controller(app).setup()


if __name__ == '__main__':
    media_api = MediaInventoryAPI()
    media_api.setup()
