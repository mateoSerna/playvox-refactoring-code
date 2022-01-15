from typing import Union

import database


# I'd use some ORM (in this case SQLAlchemy or similar) to avoid writing plain
# SQL queries. However, at least I'd create a reusable class to centralize
# the plain queries.
class Orm:
    def __init__(self):
        self.cnx = database.connection

    # I'd use static type checking to help build and maintain a cleaner architecture.
    def select_in(
        self, table: str, fields: list, where: dict, only_first: bool = False
    ) -> Union[dict, list]:
        try:
            query = self.get_query(table, fields, where)
            with self.cnx.cursor(dictionary=True, buffered=True) as cursor:
                cursor.execute(query)
                return cursor.fetchone() if only_first else cursor.fetchall()
        except Exception as e:
            # I'd use more specific exceptions.
            raise Exception(f"Error executing query: {e}")

    def get_query(self, table: str, fields: list, where: dict) -> str:
        parsed_fields = self.__parse_fields(fields)
        parsed_where = self.__parse_where(where)

        return f"SELECT {parsed_fields} FROM {table} WHERE {parsed_where}"

    @staticmethod
    def __parse_fields(fields: list) -> str:
        return ", ".join(fields)

    @staticmethod
    def __parse_where(where: dict) -> str:
        where_list = [
            f"{field} IN ({','.join(value)})" for field, value in where.items()
        ]
        return " AND ".join(where_list)
