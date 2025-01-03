import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# For one show, get the artist and track from the db

def connect_to_db(dbname, user, password, host, port):
    try:
        conn = psycopg2.connect(
            dbname=dbname, user=user,
            password=password, host=host, port=port )
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

    load_dotenv()
    db_params = {
        'dbname': os.getenv('DBNAME'), 'user': os.getenv('DBUSER'),
        'password': os.getenv('PASSWORD'), 'host': os.getenv('HOST'), 'port': os.getenv('PORT')
    }
    table_name = os.getenv('TABLENAME')

    conn = connect_to_db(**db_params)
    if conn:
        try:
            show_artist_song = get_artist_song(curr_show, table_name, conn)
        finally:
            conn.close()
    return show_artist_song
    