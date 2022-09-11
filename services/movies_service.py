from repositories.movies_repository import MoviesRepository


class MoviesService:

    def __init__(self):
        self._movie_repository = MoviesRepository()

    def list_all(self):
        return self._movie_repository.list_all()

    def list_all_paginated(self, page, size):
        offset = page * size
        return self._movie_repository.list_all_paginated(size, offset)

    def find_one(self, movie_id):
        return self._movie_repository.find_one(movie_id)
