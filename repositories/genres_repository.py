from utils.logger import Logger
from database.connection import Connection


class GenreRepository:

    def __init__(self):
        self.class_name = "GenreRepository"
        self.version = "1.0.0"

    def list_all(self):
        logger = Logger(
            class_name=self.class_name,
            function="list_all",
            version=self.version
        )

        logger.add_common_action("database_connection", "Establishing a connection to the database")
        conn = Connection()
        cnx = conn.connect()
        cursor = cnx.cursor()
        logger.finish_common_action("database_connection", True)

        query = """SELECT json_agg(js) FROM (
                            SELECT g."id",
                                   g."alias",
                                   g."reference_image"
                            FROM public."genre" g
                            ORDER BY g."alias"
                        )js;"""

        logger.add_database_action("list_genres", "List all genres", query, {})
        cursor.execute(query)
        result = cursor.fetchone()[0]
        logger.finish_database_action("list_genres", True, result)

        return result

    def list_by_movie(self, movie_id):
        logger = Logger(
            class_name=self.class_name,
            function="list_by_movie",
            version=self.version,
            parameters={
                "movieId": movie_id,
            }
        )

        logger.add_common_action("database_connection", "Establishing a connection to the database")
        conn = Connection()
        cnx = conn.connect()
        cursor = cnx.cursor()
        logger.finish_common_action("database_connection", True)

        query = """SELECT json_agg(js) FROM (
                                    SELECT g."id",
                                           g."alias",
                                           g."reference_image"
                                    FROM public."genre" g
                                    LEFT JOIN public."movie_genres" mg
                                    ON g."id" = mg."id_genre"
                                    WHERE mg."id_movie" = %(movieId)s
                                )js;"""

        params = {
            "movieId": movie_id
        }

        logger.add_database_action("list_genres_of_movie", "List all genres of a specified movie", query, params)
        cursor.execute(query, params)
        result = cursor.fetchone()[0]
        rows = 0 if result is None else len(result)
        logger.finish_database_action("list_genres_of_movie", True, rows)

        return result
