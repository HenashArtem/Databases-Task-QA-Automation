from framework.utils.logger import Logger
from mysql.connector import connect, Error


class DatabaseUtil:
    session_connection = None
    session_cursor = None

    def __init__(self, user, password, host, database):
        self._user = user
        self._password = password
        self._host = host
        self._database = database

    def create_connection(self):
        Logger.info("Creating session_connection with database")
        try:
            self.session_connection = connect(
                    host=self._host,
                    user=self._user,
                    database=self._database,
                    password=self._password)
            return self.session_connection
        except Error as err:
            Logger.error(f"Connection Error: {err}")

    def create_cursor(self, **params):
        if params is None:
            Logger.info("Creating cursor")
        else:
            Logger.info(f"Creating cursor with params: {params}")
        try:
            self.session_cursor = self.session_connection.cursor(params)
            return self.session_cursor
        except Error as err:
            Logger.error(f"Creating cursor Error: {err}")

    def close_cursor(self):
        Logger.info(f"Closing cursor")
        try:
            return self.session_cursor.close()
        except Error as err:
            Logger.error(f"Closing cursor Error: {err}")

    def close_connection(self):
        Logger.info("Closing database")
        try:
            return self.session_connection.close()
        except Error as err:
            Logger.error(f"Closing database Error: {err}")

    def send_db_query(self, query, fetchall=False):
        Logger.info(f"Creating database query: {query}")
        ""
        try:
            self.session_cursor.execute(query)
            if fetchall is True:
                data = self.session_cursor.fetchall()
                return data
            else:
                pass
        except Error as err:
            Logger.error(f"Creating database query Error: {err}")

    def send_and_commit_db_query(self, query):
        Logger.info(f"Creating and committing database query: {query}")
        try:
            with self.session_cursor as cursor:
                cursor.execute(query)
                self.session_connection.commit()
        except Error as err:
            Logger.error(f"Creating and committing database query Error: {err}")

    def select_db_data(self, column_name, name):
        self.session_cursor.execute(f"select {column_name} from {name};")
        db_res = self.session_cursor.fetchall()
        return db_res
