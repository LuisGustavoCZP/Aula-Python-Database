"""
Provides Postgres connection
"""

import psycopg2
from configs import db_configs

class Postgres:
    """
    Postgres Abstraction
    """
    def __init__(self) -> None:
        self.con = psycopg2.connect(
                    host=db_configs["host"],
                    port=db_configs["port"],
                    database=db_configs["database"],
                    user=db_configs["user"],
                    password=db_configs["password"])
        self.cursor = self.con.cursor()

    def execute (self, query:str, values:list|None = None):
        """
        Execute a basic query
        """
        if values is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, values)

    def fetch (self):
        """
        Fetch one query
        """
        return self.cursor.fetchone()

    def fetchall (self):
        """
        Fetch all queries
        """
        return self.cursor.fetchall()

    def commit (self):
        """
        Commit query
        """
        self.con.commit()

    def rollback (self):
        """
        Commit query
        """
        self.con.rollback()

    def close (self):
        """
        Close connection
        """
        self.cursor.close()
        self.con.close()
