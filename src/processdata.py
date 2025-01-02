import json
import psycopg2
from psycopg2 import sql
import os
from config.private_data import LOCAL_DATA_PATH, DBNAME, TABLENAME, USER, PASSWORD, HOST, PORT

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

    db_params = {
        'dbname': DBNAME,
        'user': USER,
        'password': PASSWORD,
        'host': HOST,
        'port': PORT
    }

    local_data_path = LOCAL_DATA_PATH
    table_name = TABLENAME

    conn = connect_to_db(**db_params)
    
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


