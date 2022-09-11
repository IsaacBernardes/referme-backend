from repositories.platforms_repository import PlatformsRepository


class PlatformsService:

    def __init__(self):
        self._platforms_repository = PlatformsRepository()

    def list_all(self):
        result = self._platforms_repository.list_all()

        if result is None:
            return []

        return result

    def list_all_by_movie(self, movie_id: int):
        result = self._platforms_repository.list_by_movie(movie_id)

        if result is None:
            return []

        return result
