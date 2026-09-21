import mysql.connector
import sys

def create_database():
    try:
        # Connect to MySQL server (without specifying database)
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password'  # Change this to your MySQL password
        )
        cursor = connection.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS attendance_system")
        print("Database 'attendance_system' created successfully!")
        
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        sys.exit(1)

if __name__ == "__main__":
    create_database()