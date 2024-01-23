import psutil
import time
from datetime import datetime
import mysql.connector

def get_usage():
    # Get CPU, memory, network, and disk usage information using psutil library
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    net_io_counters = psutil.net_io_counters()
    bytes_sent = net_io_counters.bytes_sent
    bytes_recv = net_io_counters.bytes_recv
    disk_io_counters = psutil.disk_io_counters()
    read_bytes = disk_io_counters.read_bytes
    write_bytes = disk_io_counters.write_bytes
    disk_usage = psutil.disk_usage('/')
    disk_percent = disk_usage.percent

    # Return the collected usage data
    return cpu_percent, memory_percent, bytes_sent, bytes_recv, read_bytes, write_bytes, disk_percent

def save_to_database(data):
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Mansic156918@",
            database="WHM"
        )
        cursor = connection.cursor()

        # Define the SQL query for inserting usage data into the database
        query = ("INSERT INTO usage_data (timestamp, cpu_percent, memory_percent, bytes_sent, bytes_received, "
                 "read_bytes, write_bytes, disk_percent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(query, data)

        # Commit the transaction and close the cursor and connection
        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        # Handle any exceptions that may occur during the database interaction
        print(f"Error saving to database: {e}")

if __name__ == "__main__":
    try:
        # Continuously monitor and save usage data until interrupted by the user
        while True:
            # Get the current timestamp and usage data
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            usage_data = (timestamp,) + get_usage()

            # Print the collected usage data for monitoring purposes
            print(
                f"Timestamp: {timestamp}, CPU: {usage_data[1]}%, Memory: {usage_data[2]}%, Bytes Sent: {usage_data[3]},"
                f" Bytes Received: {usage_data[4]}, Read Bytes: {usage_data[5]}, Write Bytes: {usage_data[6]}, "
                f"Disk Usage: {usage_data[7]}%")

            # Save the collected usage data to the database
            save_to_database(usage_data)

            # Wait for 1 second before collecting the next set of data
            time.sleep(1)

    except KeyboardInterrupt:
        # Handle keyboard interruption (Ctrl+C) by stopping the monitoring and displaying a message
        print("\nMonitoring stopped. Data saved to the database.")
