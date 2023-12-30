import hashlib
import sqlite3
from flask import jsonify
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
            cursor.execute(f"SELECT md5_hash, file_path, thumbnail_path FROM images ORDER BY RANDOM() LIMIT 16;")
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


    def get_thumbnail(self, image_hash):
        connection = None
        search_query =  "SELECT md5_hash, file_path, thumbnail_path "
        search_query += "FROM images WHERE "
        search_query += (f"md5_hash='{image_hash}' LIMIT 1;")

        try:
            connection = sqlite3.connect(self.database_path)
            cursor = connection.cursor()
            cursor.execute(search_query)
            result_set = cursor.fetchall()
            for row in result_set:
                print(row)
                thumbnail = Thumbnail(row[0])
                thumbnail.set_file_path(row[1])
                thumbnail.set_thumbnail_path(row[2])
                return thumbnail
        except sqlite3.Error as e:
            print(f"Thumbnail Hash Database Error: {e}, {search_query}")
            return None
        finally:
            # Close the connection
            if connection:
                connection.close()

    def search_keywords(self, search_text):
        """
        Returns a list of thumbnails matching the space-delimited search text string provided. 

        Parameters:
        - search_text: A space-delimited search string. 
        """

        all_keywords = search_text.lower().replace(",", " ").replace(".", " ").split()
        filtered_keywords = [s for s in all_keywords if not s.isdigit()]

        query =  "SELECT images.md5_hash as md5_hash, images.file_path as file_path, images.thumbnail_path as thumbnail_path FROM images INNER JOIN keywords "
        query += "ON images.id = keywords.image_id WHERE " 

        for index, keyword in enumerate(filtered_keywords):
            if index == 0:
              query += (f"keywords.keyword LIKE '{keyword}' ")
            else:
              query += (f"OR keywords.keyword LIKE '{keyword}' ")
        query += "GROUP BY 1,2 ORDER BY RANDOM();"

        connection = None
        thumbnail_list = []
        try:
            connection = sqlite3.connect(self.database_path)
            cursor = connection.cursor()
            cursor.execute(query)
            result_set = cursor.fetchall()
            print(f"DATABASE FOUND {len(result_set)} results for query {keyword}")
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



    def get_autocomplete(self, autocomplete_text):
        """
        Returns a list of thumbnails matching the autocomplete_text 

        Parameters:
        - autocomplete_text: A number of characters representing a search string. 
        """
        query =  "SELECT "
        query += "keyword "
        query += "FROM keywords "
        query += f"WHERE keywords.keyword LIKE '{autocomplete_text}%' " 
        query += "GROUP BY 1 ORDER BY RANDOM() LIMIT 1;"

        connection = None
        auto_complete = []
        try:
            connection = sqlite3.connect(self.database_path)
            cursor = connection.cursor()
            cursor.execute(query)
            result_set = cursor.fetchall()
            return jsonify(result_set[0][0])
        except sqlite3.Error as e:
            print(f"Database Error: {e}, {query}")
            return ''
        finally:
            # Close the connection
            if connection:
                connection.close() 
