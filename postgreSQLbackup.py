import psycopg2
import csv
from datetime import datetime

# Get the current timestamp
timestamp = datetime.now()

# Convert timestamp to date
date = timestamp.date()

# Print the date
print(date)

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="thingsboard",
    user="postgres",
    password="galpADMIN"
)

# Create a cursor object to execute SQL queries
cur = conn.cursor()

# Get the table names from the database
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")

# Loop over each table and write its data to a separate CSV file
for table in cur.fetchall():
    table_name = table[0]
    output_file = f"./{date}_{table_name}.csv"

    # Execute a SQL query to fetch data from the table
    cur.execute(f"SELECT * FROM {table_name}")

    # Fetch all the rows from the query result
    rows = cur.fetchall()

    # Write the data to a CSV file
    with open(output_file, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cur.description])
        csv_writer.writerows(rows)

# Close the cursor and connection
cur.close()
conn.close()
