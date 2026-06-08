#!/usr/bin/env python3
# ----------------------------------------------------------
# Template Python User Interface
# ================================
#
# Database Management Systems
# Department of Computer Science & Engineering
# University of California - Riverside
#
# Target DBMS: 'Postgres'
#
# ----------------------------------------------------------

import sys
import psycopg2


class EmbeddedSQL:
    """
    A simple embedded SQL utility class designed to work with PostgreSQL
    via the psycopg2 driver.
    """

    def __init__(self, dbname, dbport, user, passwd=""):
        """
        Creates a new instance of EmbeddedSQL and establishes a physical
        connection to the database.

        :param dbname:  the name of the database
        :param dbport:  the port the PostgreSQL server is running on
        :param user:    the user name used to login to the database
        :param passwd:  the user login password
        """
        print("Connecting to database...")
        try:
            self._connection = psycopg2.connect(
                database=dbname,
                user=user,
                password=passwd,
                host="localhost",
                port=dbport
            )
            print(f"Connection URL: postgresql://localhost:{dbport}/{dbname}\n")
            print("Done")
        except Exception as e:
            raise ConnectionError(
                f"Unable to connect to database postgresql://localhost:{dbport}/{dbname}: {e}"
            ) from e

    def execute_update(self, sql):
        """
        Executes an update SQL statement (CREATE, INSERT, UPDATE, DELETE, DROP).

        :param sql: the input SQL string
        """
        cursor = self._connection.cursor()
        cursor.execute(sql)
        self._connection.commit()
        cursor.close()

    def execute_query(self, query, params=None):
        """
        Executes a SELECT query and prints the results to standard output.

        :param query:  the input query string
        :param params: optional tuple of parameters for parameterized queries
        :return:       the number of rows returned
        """
        cursor = self._connection.cursor()
        cursor.execute(query, params)

        col_names = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        row_count = 0

        # Print header
        print("\t".join(col_names))

        # Print each row
        for row in rows:
            print("\t".join(str(val) for val in row))
            row_count += 1

        cursor.close()
        return row_count

    def cleanup(self):
        """
        Closes the physical connection if it is open.
        """
        try:
            if self._connection is not None:
                self._connection.close()
        except Exception:
            pass  # ignored


# ----------------------------------------------------------
# Helper functions
# ----------------------------------------------------------

def greeting():
    print("\n\n*******************************************************")
    print("              User Interface                           ")
    print("*******************************************************\n")


def read_choice():
    """
    Reads the user's menu choice from the keyboard.
    Keeps prompting until a valid integer is entered.
    """
    while True:
        try:
            return int(input("Please make your choice: "))
        except ValueError:
            print("Your input is invalid!")


# ----------------------------------------------------------
# Query functions
# ----------------------------------------------------------

def query_example(esql):
    """Example query: find parts with cost lower than a user-supplied value."""
    try:
        cost = input("\tEnter cost: $")
        row_count = esql.execute_query(
            "SELECT * FROM Catalog WHERE cost < %s;",
            (cost,)
        )
        print(f"total row(s): {row_count}")
    except Exception as e:
        print(e, file=sys.stderr)


def query1(esql):
    # Your code goes here.
    # ...
    # ...
    cursor = esql._connection.cursor()
    cursor.execute("SELECT s.sname, COUNT(c.pid) AS total_parts FROM SUPPLIERS s JOIN CATALOG c ON s.sid = c.sid GROUP BY s.sname;")
    col_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    for row in rows:
        for col, val in zip(col_names, row):
            print(col, "=", val)
        print()
    cursor.close()
    pass


def query2(esql):
    # Your code goes here.
    # ...
    # ...
    cursor = esql._connection.cursor()
    cursor.execute("SELECT s.sname, COUNT(c.pid) AS total_parts FROM SUPPLIERS s JOIN CATALOG c ON s.sid = c.sid GROUP BY s.sname HAVING COUNT(c.pid) >= 3;")
    col_names = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    for row in rows:
        for col, val in zip(col_names, row):
            print(col, "=", val)
        print()
    cursor.close()
    pass


def query3(esql):
    # Your code goes here.
    # ...
    # ...
    try:
        row_count = esql.execute_query(
            "SELECT s.sname, COUNT(c.pid) AS total_parts FROM SUPPLIERS s JOIN CATALOG c ON s.sid = c.sid JOIN parts p ON c.pid = p.pid GROUP BY s.sname HAVING COUNT(*) = SUM(CASE WHEN p.color = 'Green' THEN 1 ELSE 0 END);"
        )
        print(f"total row(s): {row_count}")
    except Exception as e:
        print(e, file=sys.stderr)
    pass


def query4(esql):
    # Your code goes here.
    # ...
    # ...
    try:
        row_count = esql.execute_query(
            "SELECT s.sname, MAX(c.cost) AS expensive_part FROM SUPPLIERS s JOIN CATALOG c ON s.sid = c.sid JOIN parts p ON c.pid = p.pid GROUP BY s.sname HAVING SUM(CASE WHEN p.color = 'Green' THEN 1 ELSE 0 END) > 0 AND SUM(CASE WHEN p.color = 'Red' THEN 1 ELSE 0 END) > 0;"
        )
        print(f"total row(s): {row_count}")
    except Exception as e:
        print(e, file=sys.stderr)
    pass


def query5(esql):
    # Your code goes here.
    # ...
    # ...
    try:
        cost = input("\tEnter cost: $")
        row_count = esql.execute_query(
            "SELECT p.pname FROM Catalog c JOIN Parts p ON c.pid = p.pid WHERE c.cost < %s;",
            (cost,)
        )
        print(f"total row(s): {row_count}")
    except Exception as e:
        print(e, file=sys.stderr)
    pass


def query6(esql):
    # Your code goes here.
    # ...
    # ...
    try:
        product_name = input("\tEnter product name: ")
        row_count = esql.execute_query(
            "SELECT address FROM SUPPLIERS WHERE sid IN (SELECT sid FROM CATALOG WHERE pid = (SELECT pid FROM PARTS WHERE pname = %s));",
            (product_name,)
        )
        print(f"total row(s): {row_count}")
    except Exception as e:
        print(e, file=sys.stderr)
    pass


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------

def main():
    if len(sys.argv) != 4:
        print(
            f"Usage: python {sys.argv[0]} <dbname> <port> <user>",
            file=sys.stderr
        )
        return

    greeting()

    dbname = sys.argv[1]
    dbport = sys.argv[2]
    user   = sys.argv[3]

    esql = None
    try:
        esql = EmbeddedSQL(dbname, dbport, user, "")

        keepon = True
        while keepon:
            print("MAIN MENU")
            print("---------")
            print("0. Find the pid of parts with cost lower than $_____ (example)")
            print("1. Find the total number of parts supplied by each supplier")
            print("2. Find the total number of parts supplied by each supplier who supplies at least 3 parts")
            print("3. For every supplier that supplies only green parts, print the name of the supplier and the total number of parts that they supply")
            print("4. For every supplier that supplies green part and red part, print the name and the price of the most expensive part that they supply")
            print("5. Find the name of parts with cost lower than $_____")
            print("6. Find the address of the suppliers who supply _____________ (pname)")
            print("9. < EXIT")

            choice = read_choice()

            if   choice == 0: query_example(esql)
            elif choice == 1: query1(esql)
            elif choice == 2: query2(esql)
            elif choice == 3: query3(esql)
            elif choice == 4: query4(esql)
            elif choice == 5: query5(esql)
            elif choice == 6: query6(esql)
            elif choice == 9: keepon = False
            else: print("Unrecognized choice!")

    except Exception as e:
        print(e, file=sys.stderr)
    finally:
        if esql is not None:
            print("Disconnecting from database...", end="")
            esql.cleanup()
            print("Done\n\nBye!")


if __name__ == "__main__":
    main()
