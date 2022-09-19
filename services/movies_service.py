from models.Movie import Movie
from repositories.movies_repository import MoviesRepository


class MoviesService:

    def __init__(self):
        self._movie_repository = MoviesRepository()

    def list_all(self):
        return self._movie_repository.list_all()

    def list_popular(self):
        return self._movie_repository.list_popular()

    def list_all_paginated(self, page, size):
        offset = page * size
        return self._movie_repository.list_all_paginated(size, offset)

    def find_one(self, movie_id):
        return self._movie_repository.find_one(movie_id)

    def insert_movie(self, movie: Movie):
        return self._movie_repository.insert_movie(movie)
