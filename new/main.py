import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os, sys

def load_db_params():
    load_dotenv()
    return {
        'dbname': os.getenv('DBNAME'), 'user': os.getenv('DBUSER'),
        'password': os.getenv('PASSWORD'), 'host': os.getenv('HOST'), 'port': os.getenv('PORT')
    }

def connect_to_db(db_params):
    try:
        conn = psycopg2.connect(**db_params)
        return conn
    except psycopg2.Error as e: 
        print(f'Error: could not connect to the database: {e}')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')


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
    db_params = load_db_params()
    table_name = os.getenv('TABLENAME')

    conn = connect_to_db(db_params)
    if conn:
        try:
            show_artist_song = get_artist_song(curr_show, table_name, conn)
        finally:
            conn.close()
    return show_artist_song

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
    db_params = load_db_params()
    table_name = 'show_date'
    conn = connect_to_db(db_params)
    if conn:
        try:
            show_number = get_show_number(show_date, table_name, conn)
            if show_number is None:
                print(f"No show found for {show_date}")
        finally:
            conn.close()
    return show_number

if __name__ == '__main__':
    # User supplies a date at the command line in ISO format
    show_date = sys.argv[1]
    # From that date, get the show number
    show_number = pick_show_date(show_date)
    # Get the artist and song for the show, from file get_songs_fromshow.py
    show_artist_song = process_current_show(show_number)
    print(show_artist_song)

