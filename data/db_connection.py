import sys

import psycopg2
import psycopg2.extras

DB_CONFIG = {"dbname": "", "dbport": "", "user": "", "passwd": ""}


class EmbeddedSQL:
    """Small PostgreSQL helper class for Flask query functions."""

    def __init__(self, dbname, dbport, user, passwd=""):
        try:
            self._connection = psycopg2.connect(
                database=dbname,
                user=user,
                password=passwd,
                host="localhost",
                port=dbport,
            )
        except Exception as e:
            print(f"Error - Unable to Connect to Database: {e}", file=sys.stderr)
            raise

    def execute_query(self, query, params=None):
        cursor = self._connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, params)
        rows = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        return rows

    def execute_one(self, query, params=None):
        cursor = self._connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, params)
        row = cursor.fetchone()
        cursor.close()
        return dict(row) if row else None

    def execute_update(self, sql, params=None):
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        affected = cursor.rowcount
        self._connection.commit()
        cursor.close()
        return affected

    def cleanup(self):
        try:
            if self._connection is not None:
                self._connection.close()
        except Exception:
            pass
