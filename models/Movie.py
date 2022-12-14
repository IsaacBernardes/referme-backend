class Movie:
    
    def __init__(self):
        self.name = None
        self.synopsis = None
        self.rating = None
        self.image_url = None
        self.popular = False
        self.genres = []

    def set_name(self, name: str):
        self.name = name
        return self

    def set_synopsis(self, synopsis: str):
        self.synopsis = synopsis
        return self

    def set_rating(self, rating: float):
        self.rating = rating
        return self

    def set_image(self, image: str):
        self.image_url = image
        return self

    def set_popular(self, popular: bool):
        self.popular = popular
        return self

    def set_genres(self, genres: list[str]):
        self.genres = genres
        return self
