import sqlite3
from sqlite3 import Error

# https://www.sqlitetutorial.net/sqlite-python/creating-database/

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_annotation(conn, task):
    sql = ''' INSERT INTO annotations(image,annotation,object)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

    return cur.lastrowid

def select_all_annotations(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM annotations")

    rows = cur.fetchall()

    return rows

def select_annotations_by_image_name(conn, image):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM annotations WHERE image=?", (image,))

    rows = cur.fetchall()

    return rows

# -- Queries
sql_create_annotations_table = """CREATE TABLE IF NOT EXISTS annotations (
                                    id integer PRIMARY KEY,
                                    image text NOT NULL,
                                    annotation text NOT NULL,
                                    object text NOT NULL
                                );"""