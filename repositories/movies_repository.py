from models.Movie import Movie
from utils.logger import Logger
from database.connection import Connection


class MoviesRepository:

    def __init__(self):
        self.class_name = "MovieRepository"
        self.version = "1.0.0"

    def list_all(self):
        logger = Logger(class_name=self.class_name, function="list_all", version=self.version)

        logger.add_common_action("database_connection", "Establishing a connection to the database")
        conn = Connection()
        cnx = conn.connect()
        cursor = cnx.cursor()
        logger.finish_common_action("database_connection", True)

        query = """SELECT json_agg(js) FROM (
                            SELECT m."id",
                                   m."name",
                                   m."synopsis",
                                   m."rating" as "score",
                                   m."image_url" as "image",
                                   m."trailer_url" as "trailerURL",
                                   m."popular" as "popular"
                            FROM public."movie" m
                            ORDER BY m."name"
                        )js;"""

        logger.add_database_action("list_movies", "List movies with limits", query, {})
        cursor.execute(query)
        result = cursor.fetchone()[0]
        logger.finish_database_action("list_movies", True, len(result))

        return result

    def list_popular(self):
        logger = Logger(class_name=self.class_name, function="list_popular", version=self.version)

        logger.add_common_action("database_connection", "Establishing a connection to the database")
        conn = Connection()
        cnx = conn.connect()
        cursor = cnx.cursor()
        logger.finish_common_action("database_connection", True)

        query = """SELECT json_agg(js) FROM (
                            SELECT m."id",
                                   m."name",
                                   m."synopsis",
                                   m."rating" as "score",
                                   m."image_url" as "image",
                                   m."trailer_url" as "trailerURL",
                                   m."popular" as "popular",
                                   ARRAY_AGG(g."alias") AS "genres"
                            FROM public."movie" m, public."genre" g, public."movie_genres" mg
                            WHERE m."popular" IS TRUE AND g."id" = mg."id_genre"
                            AND mg."id_movie" = m."id"
                            GROUP BY m."id" ORDER BY m."name"
                        )js;"""

        logger.add_database_action("list_movies", "List movies with limits", query, {})
        cursor.execute(query)
        result = cursor.fetchone()[0]
        logger.finish_database_action("list_movies", True, len(result))

        return result

    def list_all_paginated(self, limit=100, offset=0):
        logger = Logger(
            class_name=self.class_name,
            function="list_all_paginated",
            version=self.version,
            parameters={
                "limit": limit,
                "offset": offset
            }
        )

        logger.add_common_action("database_connection", "Establishing a connection to the database")
        conn = Connection()
        cnx = conn.connect()
        cursor = cnx.cursor()
        logger.finish_common_action("database_connection", True)

        query = """SELECT json_agg(js) FROM (
                    SELECT m."id",
                           m."name",
                           m."synopsis",
                           m."rating" as "score",
                           m."image_url" as "image",
                           m."trailer_url" as "trailerURL",
                           m."popular" as "popular"
                    FROM public."movie" m
                    ORDER BY m."name"
                    LIMIT %(limit)s
                    OFFSET %(offset)s
                )js;"""

        params = {
            "limit": limit,
            "offset": offset
        }

        logger.add_database_action("list_some_movies", "List movies with limits", query, params)
        cursor.execute(query, params)
        result = cursor.fetchone()[0]
        logger.finish_database_action("list_some_movies", True, len(result))

        logger.save()

        return result

    def find_one(self, movie_id):
        logger = Logger(
            class_name=self.class_name,
            function="find_one",
            version=self.version,
            parameters={
                "movieId": movie_id
            }
        )

        logger.add_common_action("database_connection", "Establishing a connection to the database")
        conn = Connection()
        cnx = conn.connect()
        cursor = cnx.cursor()
        logger.finish_common_action("database_connection", True)

        query = """SELECT json_agg(js) FROM (
                            SELECT m."id",
                                   m."name",
                                   m."synopsis",
                                   m."rating" as "score",
                                   m."image_url" as "image",
                                   m."trailer_url" as "trailerURL"
                            FROM public."movie" m
                            WHERE m."id" = %(movieId)s
                            LIMIT 1
                        )js;"""

        params = {
            "movieId": movie_id
        }

        logger.add_database_action("find_movie", "Find movie by ID", query, params)
        cursor.execute(query, params)
        result = cursor.fetchone()[0]
        logger.finish_database_action("find_movie", True, len(result))

        if len(result) > 0:
            result = result[0]

        return result

    def insert_movie(self, movie: Movie):
        logger = Logger(
            class_name=self.class_name,
            function="insert_movie",
            version=self.version,
            parameters={
                "movie": movie
            }
        )

        logger.add_common_action("database_connection", "Establishing a connection to the database")
        conn = Connection()
        cnx = conn.connect()
        cursor = cnx.cursor()
        logger.finish_common_action("database_connection", True)

        query = """SELECT json_agg(js) FROM (
                            SELECT m."id"
                            FROM public."movie" m
                            WHERE m."name" = %(name)s
                        )js;"""

        params = {
            "name": movie.name,
            "synopsis": movie.synopsis,
            "rating": movie.rating,
            "image_url": movie.image_url,
            "popular": movie.popular
        }

        logger.add_database_action("find_movie", "Find movie by name", query, params)
        cursor.execute(query, params)
        result = cursor.fetchone()[0]
        logger.finish_database_action("find_movie", True)

        if result is not None and len(result) > 0:
            logger.add_exception("Movie already exists")
            return None

        query = """INSERT INTO public."movie" ("name", "synopsis", "rating", "image_url", "popular")
                   VALUES (%(name)s, %(synopsis)s, %(rating)s, %(image_url)s, %(popular)s)
                   RETURNING json_build_object(
                       'id', id,
                       'name', name,
                       'synopsis', synopsis,
                       'score', rating,
                       'image', image_url,
                       'trailerURL', trailer_url,
                       'popular', popular
                   );
                   """

        logger.add_database_action("insert_movie", "Insert movie", query, params)
        cursor.execute(query, params)
        movie_object = cursor.fetchone()[0]
        cnx.commit()
        logger.finish_database_action("insert_movie", True)

        if movie_object is not None and len(movie.genres) > 0:

            query = """SELECT g."id" FROM public."genre" g
                       WHERE LOWER(g."alias") LIKE ANY(%(genres)s);"""

            params = {
                "genres": ["%" + str(x).lower() + "%" for x in movie.genres]
            }

            cursor.execute(query, params)
            genre_id_list = cursor.fetchone()

            if genre_id_list is None:
                return movie_object

            query = """INSERT INTO "movie_genres" ("id_movie", "id_genre") VALUES"""
            for genre_id in genre_id_list:
                query += f" ({movie_object['id']}, {genre_id}),"
            query = query[:-1] + ";"

            cursor.execute(query)
            cnx.commit()

        return movie_object
