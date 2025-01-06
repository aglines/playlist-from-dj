import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
from fuzzywuzzy import process

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

def get_distinct_artist_and_counts(db_params, table_name):
    conn = connect_to_db(**db_params)
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    sql.SQL(
                        # 'SELECT DISTINCT artist FROM {table} ORDER BY artist LIMIT 100'
                        'SELECT DISTINCT artist FROM {table} ORDER BY artist'

                    ).format(
                        table=sql.Identifier(table_name)
                    )
                )
                distinct_artistname = cursor.fetchall()

                cursor.execute(
                    sql.SQL(
                        'SELECT artist, COUNT(*) as count FROM {table} GROUP BY artist'
                        # 'SELECT artist, COUNT(*) as count FROM {table} GROUP BY artist ORDER BY count desc LIMIT 100'

                    ).format(
                        table=sql.Identifier(table_name)
                    )
                )
                distinct_artistcounts = cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error: Could not get data from the table. {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            conn.close()
    return distinct_artistname, distinct_artistcounts

def find_highest_match(distinct_artistnames, distinct_artistcounts):
    # Step 1: Initialize Data Structures
    correct_names = {artist: count for artist, count in distinct_artistcounts}
    corrected_names = {}

    # Step 2: Fuzzy Matching
    for artist_tuple in distinct_artistnames:
        artist = artist_tuple[0]  # Extract the artist name from the tuple
        if artist not in correct_names:
            # Find the closest match
            closest_match, _ = process.extractOne(artist, correct_names.keys())
            corrected_names[artist] = closest_match
        else:
            corrected_names[artist] = artist

    return corrected_names

    
def main():
    load_dotenv()
    db_params = {
        'dbname': os.getenv('DBNAME'), 'user': os.getenv('DBUSER'),
        'password': os.getenv('PASSWORD'), 'host': os.getenv('HOST'), 'port': os.getenv('PORT')
    }
    table_name = os.getenv('TABLENAME')

    # get a list of distinct artist names and their counts
    distinct_artistnames, distinct_artistcounts = get_distinct_artist_and_counts(db_params, table_name)

    # find the correct spelling of the artist names
    corrected_names = find_highest_match(distinct_artistnames, distinct_artistcounts)
    # print(corrected_names)


if __name__ == '__main__':
    main()
