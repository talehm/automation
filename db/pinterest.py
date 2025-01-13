import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from db.connection import create_connection

# Load environment variables from the .env file
load_dotenv()


class PinterestLinkDatabase:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Establishes connection to the MySQL database."""
        try:
            self.connection, self.cursor = create_connection()
            if self.connection is None or self.cursor is None:
                print("Failed to establish a valid connection and cursor.")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            self.connection = None
            self.cursor = None

    def insert_pinterest_link(
        self,
        post_id,
        link,
        title,
        description,
        media_url,
        board_id,
        board_section_id,
        alt_text,
        keywords,
    ):
        """Inserts a new row into the pinterest_link table if the post_id doesn't already exist."""
        try:
            # Check if the post_id already exists in the pinterest_link table
            self.cursor.execute(
                "SELECT COUNT(*) FROM pinterest_link WHERE post_id = %s", (post_id,)
            )
            result = self.cursor.fetchone()

            # If post_id exists, do not insert, or handle as needed
            if result[0] > 0:
                print(f"Post with ID {post_id} already exists. Skipping insert.")
                return  # You can also choose to update the record instead

            # SQL query to insert data into the table if post_id doesn't exist
            query = """
            INSERT INTO pinterest_link (post_id, link, title, description, media_url, board_id, board_section_id, alt_text, keywords)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Execute the query with the given data
            self.cursor.execute(
                query,
                (
                    post_id,
                    link,
                    title,
                    description,
                    media_url,
                    board_id,
                    board_section_id,
                    alt_text,
                    keywords,
                ),
            )
            self.connection.commit()  # Commit the transaction
            print(f"Successfully inserted row: {title}")
        except Error as e:
            print(f"Error while inserting data: {e}")
            self.connection.rollback()  # Rollback in case of error

    def close(self):
        """Closes the connection to the database."""
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Connection closed.")

    def exists(self, id):
        if self.connection.is_connected():
            self.cursor.execute(
                "SELECT COUNT(*) FROM pinterest_link WHERE post_id = %s", (id,)
            )
            result = self.cursor.fetchone()

            # If post_id exists, do not insert, or handle as needed
            if result[0] > 0:
                print(f"Post with ID {id} already exists. Skipping insert.")
                return True
            return False

    def get_items(self, limit=20):
        if self.connection.is_connected():
            self.cursor.execute(
                f"SELECT * FROM pinterest_link WHERE is_shared = 0 limit {limit};"
            )
            result = self.cursor.fetchall()

            # If post_id exists, do not insert, or handle as needed
            # if result > 0:
            #     print(f"Post with ID {id} already exists. Skipping insert.")
            #     return True
            return result

    def set_as_published(self, id):
        if self.connection.is_connected():
            self.cursor.execute(
                "UPDATE pinterest_link SET is_shared = %s WHERE _id = %s", (1, id)
            )
            self.connection.commit()
            # result    = self.cursor.fetchone()
            rows_updated = self.cursor.rowcount  # Number of rows updated
            # If post_id exists, do not insert, or handle as needed
            # if result > 0:
            #     print(f"Post with ID {id} already exists. Skipping insert.")
            #     return True
            return rows_updated
