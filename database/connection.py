import os
import psycopg2


class Connection:
    def __init__(self):
        self.host = os.environ["DB_HOST"]
        self.port = os.environ["DB_PORT"]
        self.name = os.environ["DB_NAME"]
        self.user = os.environ["DB_USER"]
        self.password = os.environ["DB_PASSWORD"]

    def connect(self) -> psycopg2._psycopg.connection:
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            dbname=self.name,
            user=self.user,
            password=self.password
        )
