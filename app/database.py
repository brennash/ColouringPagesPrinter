import hashlib
import sqlite3
from .thumbnail import Thumbnail
from PIL import Image


class Database:

    def __init__(self):
        self.thumbnails = []
        self.database_path = 'app/colouring_pages.db'



    def get_thumbnail_list(self):
        connection = None
        insert_query = None
        thumbnail_list = []
        try:
            connection = sqlite3.connect(self.database_path)
            cursor = connection.cursor()
            cursor.execute(f"SELECT md5_hash, file_path, thumbnail_path FROM images ORDER BY total_selections DESC, last_selected_yyyymmdd DESC;")
            result_set = cursor.fetchall()
            for row in result_set:
                print(row)
                thumbnail = Thumbnail(row[0])
                thumbnail.set_file_path(row[1])
                thumbnail.set_thumbnail_path(row[2])
                thumbnail_list.append(thumbnail)
            return thumbnail_list
        except sqlite3.Error as e:
            print(f"Database Error: {e}, {insert_query}")
            return thumbnail_list
        finally:
            # Close the connection
            if connection:
                connection.close()     
