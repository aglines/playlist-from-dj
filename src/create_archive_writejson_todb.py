import json
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

def read_json_files(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f'File not found: {file_path}')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

def connect_to_db(dbname, user, password, host, port):
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        return conn
    except psycopg2.Error as e: 
        print(f'Error: could not connect to the database: {e}')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

def create_table(conn, table_name):
    try:
        with conn.cursor() as cursor:
            create_table_query = sql.SQL(
                """
                CREATE TABLE IF NOT EXISTS {table} (
                id SERIAL PRIMARY KEY,
                uri text COLLATE pg_catalog."default",
                airdate timestamp without time zone,
                show integer,
                show_uri text COLLATE pg_catalog."default",
                image_uri text COLLATE pg_catalog."default",
                thumbnail_uri text COLLATE pg_catalog."default",
                song text COLLATE pg_catalog."default",
                track_id text COLLATE pg_catalog."default",
                recording_id text COLLATE pg_catalog."default",
                artist text COLLATE pg_catalog."default",
                artist_ids text COLLATE pg_catalog."default",
                album text COLLATE pg_catalog."default",
                release_id text COLLATE pg_catalog."default",
                release_group_id text COLLATE pg_catalog."default",
                labels text COLLATE pg_catalog."default",
                label_ids text COLLATE pg_catalog."default",
                release_date date,
                rotation_status text COLLATE pg_catalog."default",
                is_local boolean,
                is_request boolean,
                is_live boolean,
                location integer,
                location_name text COLLATE pg_catalog."default",
                comment text COLLATE pg_catalog."default",
                play_type text COLLATE pg_catalog."default",
                is_already_in_spotify_tracks boolean DEFAULT false
                )
                """
            ).format(table=sql.Identifier(table_name))
            cursor.execute(create_table_query)
            conn.commit()
            print(f"Table {table_name} created successfully.")
    except psycopg2.Error as e:
        print(f"Error: Could not create table {table_name}. {e}")
        conn.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        conn.rollback()


def insert_data(conn, data, table_name):
    try:
        with conn.cursor() as cursor:
            for record in data:
                columns = record.keys()

                values = []
                for column in columns:
                    value = record[column]
                    if isinstance(value, (list, dict)):
                        value = json.dumps(value)
                    values.append(value)

                insert_statement = sql.SQL(
                    'INSERT INTO {table} ({fields}) VALUES ({values})'
                ).format(
                    table=sql.Identifier(table_name),
                    fields=sql.SQL(', ').join(map(sql.Identifier, columns)),
                    values=sql.SQL(', ').join(map(sql.Placeholder, columns))
                )
                cursor.execute(insert_statement, record)
            conn.commit()
    except psycopg2.Error as e:
        print(f"Error: Could not insert data into the table. {e}")
        conn.rollback()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        conn.rollback()

def main():
    load_dotenv()

    db_params = {
        'dbname': os.getenv('DBNAME'), 'user': os.getenv('DBUSER'),
        'password': os.getenv('PASSWORD'), 'host': os.getenv('HOST'), 'port': os.getenv('PORT')
    }
    table_name = os.getenv('TABLENAME')
    local_data_path = os.getenv('LOCAL_DATA_PATH')

    conn = connect_to_db(**db_params)
    
    create_table(conn, table_name)

    for file_name in os.listdir(local_data_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(local_data_path, file_name)
            print(f'Reading file: {file_name}')

            data = read_json_files(file_path)
            if data is None:
                continue

            insert_data(conn, data, table_name)
    
    conn.close()

if __name__ == '__main__':
    main()


