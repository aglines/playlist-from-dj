import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os, sys
from contextlib import contextmanager

def load_db_params():
    load_dotenv()
    return {
        'dbname': os.getenv('DBNAME'), 'user': os.getenv('DBUSER'),
        'password': os.getenv('PASSWORD'), 'host': os.getenv('HOST'), 'port': os.getenv('PORT')
    }

@contextmanager
def get_db_connection():
    db_params = load_db_params()
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        yield conn
    except psycopg2.Error as e:
        print(f'Error: could not connect to the database: {e}')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
    finally:
        if conn:
            conn.close()

def get_artist_song(show, table_name, conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL(
                    'SELECT artist, song FROM {table} WHERE show = {show}'
                ).format(
                    table=sql.Identifier(table_name),
                    show=sql.Literal(show)
                )
            )
            rows = cursor.fetchall()
    except psycopg2.Error as e:
        print(f"Error: Could not get data from the table. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return rows

def process_current_show(curr_show):
    table_name = os.getenv('TABLENAME')
    with get_db_connection() as conn:
        return get_artist_song(curr_show, table_name, conn)

def get_show_number(show_date, table_name, conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL(
                    'SELECT show_id FROM {table} WHERE date = {show_date}'
                ).format(
                    table=sql.Identifier(table_name),
                    show_date=sql.Literal(show_date)
                )
            )
            row = cursor.fetchone()
            show_id = row[0] if row else None
    except psycopg2.Error as e:
        print(f"Error: Could not get data from the table. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return show_id

def pick_show_date(show_date):
    table_name = 'show_date'
    with get_db_connection() as conn:
        show_number = get_show_number(show_date, table_name, conn)
        return show_number
