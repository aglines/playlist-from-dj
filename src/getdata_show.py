import psycopg2
from psycopg2 import sql

from config.private_data import LOCAL_DATA_PATH, DBNAME, TABLENAME, USER, PASSWORD, HOST, PORT

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
            print(rows)
            return rows
    except psycopg2.Error as e:
        print(f"Error: Could not get data from the table. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():

    # Pick one show at random
    curr_show = 37547

    db_params = {
        'dbname': DBNAME, 'user': USER,
        'password': PASSWORD, 'host': HOST, 'port': PORT
    }
    local_data_path = LOCAL_DATA_PATH
    table_name = TABLENAME

    conn = connect_to_db(**db_params)

    # Get the artist and track for the show
    get_artist_song(curr_show, table_name, conn)

if __name__ == '__main__':
    main()
