"""
MySQL connector variant — swap this in place of SQLite
by changing get_connection() in admin_panel.py
"""

import mysql.connector

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "your_database"
}


def get_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)


def get_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    return [row[0] for row in cursor.fetchall()]


def get_columns(conn, table):
    cursor = conn.cursor()
    cursor.execute(f"DESCRIBE {table}")
    # Returns: (name, type, null, key, default, extra)
    return cursor.fetchall()


def get_all_rows(conn, table):
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM {table}")
    return cursor.fetchall()
