from utils.logger import Logger
from database.connection import Connection


class PlatformsRepository:

    def __init__(self):
        self.class_name = "PlatformRepository"
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
                            SELECT p."id",
                                   p."name",
                                   p."url"
                            FROM public."platform" p
                            ORDER BY p."name"
                        )js;"""

        logger.add_database_action("list_platforms", "List all platforms", query, {})
        cursor.execute(query)
        result = cursor.fetchone()[0]
        logger.finish_database_action("list_platforms", True, len(result))

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
                                    SELECT p."id",
                                           p."name",
                                           p."url"
                                    FROM public."platform" p
                                    LEFT JOIN public."movie_platforms" mg
                                    ON p."id" = mg."id_platform"
                                    WHERE mg."id_movie" = %(movieId)s
                                )js;"""

        params = {
            "movieId": movie_id
        }

        logger.add_database_action("list_platforms_by_movie", "List all platforms of a specified movie", query, params)
        cursor.execute(query, params)
        result = cursor.fetchone()[0]
        logger.finish_database_action("list_genres_of_movie", True, len(result))

        return result
