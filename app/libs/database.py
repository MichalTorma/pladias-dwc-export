# database.py
import os
import psycopg2
import csv

def query_to_csv(sql_query, csv_file_path):
    """
    Executes a SQL query on a PostgreSQL database and exports the results to a CSV file.

    Parameters:
    - sql_query: The SQL query to execute.
    - csv_file_path: The path to save the CSV file.
    """
    # Environment variables for PostgreSQL credentials
    db_host = os.environ.get('DB_HOST')
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)

    # Execute the query and fetch results
    cur = conn.cursor()
    cur.execute(sql_query)
    rows = cur.fetchall()

    # Export query results to CSV
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([desc[0] for desc in cur.description])  # write headers
        csv_writer.writerows(rows)

    # Clean up
    cur.close()
    conn.close()
