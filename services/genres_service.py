from repositories.genres_repository import GenreRepository


class GenresService:

    def __init__(self):
        self._genre_repository = GenreRepository()

    def list_all(self):
        result = self._genre_repository.list_all()

        if result is None:
            return []

        return result

    def list_all_by_movie(self, movie_id: int):
        result = self._genre_repository.list_by_movie(movie_id)

        if result is None:
            return []

        return result
