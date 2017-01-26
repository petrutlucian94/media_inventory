import logging
from flask import request

from media_inventory.models import movie as movie_model
from media_inventory.api.controllers import base as base_controller

LOG = logging.getLogger('media_inventory')


class MoviesController(base_controller.BaseAPIController):
    def setup(self):
        self._ensure_root_node_exists()

        self.setup_routes()

    def setup_routes(self):
        self._app.add_url_rule('/movies',
                               methods=['GET'],
                               view_func=self.get_movies)
        self._app.add_url_rule('/movies/<movie_id>',
                               methods=['GET'],
                               view_func=self.get_movie)
        self._app.add_url_rule('/movies',
                               methods=['POST'],
                               view_func=self.add_movie)
        self._app.add_url_rule('/movies',
                               methods=['PUT'],
                               view_func=self.update_movie)
        self._app.add_url_rule('/movies/<movie_id>',
                               methods=['DELETE'],
                               view_func=self.delete_movie)

    def get_movies(self):
        LOG.debug("Got request to fetch all movies")
        return self._db_api.query('/inventory/movies')

    def get_movie(self, movie_id):
        LOG.debug("Got request to fetch movie %s" % movie_id)
        return self._db_api.query('/inventory/movies/movie[@id="%s"]' % movie_id)

    def _get_movie_from_request(self):
        self.validate_request(schema_name='movie')
        request_body = request.get_data()
        movie = movie_model.Movie(request_body)

        return movie

    def add_movie(self):
        LOG.debug("Got request to add movie: %s" % request.data)

        movie = self._get_movie_from_request()

        self._db_api.insert(movie.to_xml(), '/inventory/movies')

        return movie.to_xml()

    def update_movie(self):
        LOG.debug("Got request to update movie: %s" % request.data)

        movie = self._get_movie_from_request()

        self.delete_movie(movie.id)
        self.add_movie(movie.to_xml())

        return movie.to_xml()

    def delete_movie(self, movie_id):
        LOG.debug("Got request to delete movie: %s" % movie_id)

        self._db_api.query(
            'delete node /inventory/movies/movie[@id="%s"]' % movie_id)

        return ''

    def _ensure_root_node_exists(self):
        if not self.get_movies():
            self._db_api.insert('<movies></movies>', '/inventory')       
