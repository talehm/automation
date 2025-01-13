import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os


def create_connection():
    load_dotenv()

    """Establishes connection to the MySQL database."""
    try:
        # Replace the placeholders with your actual database credentials
        port_value = os.getenv("DB_PORT", "3306").split()[
            0
        ]  # Split on space and take the first part
        port = int(port_value)  # Convert to integer
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=port,
        )

        if connection.is_connected():
            cursor = connection.cursor()

            print("Connected to the MySQL database!")
            return connection, cursor
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


def insert_data():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO pinterest_link (title, description, url, board_id, board_section_id, alt_text, keywords ) VALUES ('title', 'description','url',1,2,'fdfd','dfdfd')"
            )
            connection.commit()
            print("Data inserted successfully")

        except Exception as e:
            print(f"Error inserting data: {e}")

        finally:
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
