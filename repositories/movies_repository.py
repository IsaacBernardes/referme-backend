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
                                   m."rating"/2 as "score",
                                   m."image_url" as "image",
                                   m."trailer_url" as "trailerURL"
                            FROM public."movie" m
                            ORDER BY m."name"
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
                           m."rating"/2 as "score",
                           m."image_url" as "image",
                           m."trailer_url" as "trailerURL"
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
                                   m."rating"/2 as "score",
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

