import json
import psycopg2
from psycopg2 import sql

# Connection parameters
db_params = {
    'dbname': 'bibliake',
    'user': 'postgres',
    'password': '141778215aA!',
    'host': 'bible-study.c5s2qwqc2jwx.eu-north-1.rds.amazonaws.com',
    'port': '5432',
}

# Replace the above placeholders with your actual database connection details

# JSON file path
json_file_path = 'D:\CMS\Church\BibleStudy\kjv.json'

def connect_to_database():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_params)
    return conn

def populate_king_james_version_table(conn, data):
    # Insert data into the 'KingJamesVersionI' table
    with conn.cursor() as cursor:
        for item in data['resultset']['row']:
            field_values = item['field']
            print(field_values[-1])

            # Use psycopg2.sql.SQL to safely compose SQL queries
            insert_query = sql.SQL("INSERT INTO {} (book, chapter, verse, text) VALUES (%s, %s, %s, %s)").format(
                sql.Identifier("BibleStudy_kingjamesversioni")
            )

            # Use cursor.mogrify to escape values and prevent SQL injection
            cursor.execute(cursor.mogrify(insert_query, (
                field_values[1],
                field_values[2],
                field_values[3],
                field_values[4],
            )))
            conn.commit()

def main():
    try:
        # Read JSON file
        with open(json_file_path) as json_file:
            data = json.load(json_file)

        # Connect to the PostgreSQL database
        connection = connect_to_database()

        # Populate the 'KingJamesVersionI' table with data from the JSON file
        populate_king_james_version_table(connection, data)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the database connection
        if connection:
            connection.close()

main()
