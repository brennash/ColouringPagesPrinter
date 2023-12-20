import os
import re
import csv
import sys
import sqlite3
import datetime
from PIL import Image
import hashlib
from optparse import OptionParser

class ImportImages:

	def __init__(self, updateFlag=False):
		self.update = updateFlag
		self.thumbnail_height = 200
		self.image_height = 850

		if self.update == False:
			print("Database will not be updated, unless you set the -u|--update command line option")
			self.database_path = None
		else:
			self.database_path = 'app/colouring_pages.db'
			self.clean_database_table('images')
			self.clean_database_table('keywords')
			self.clean_database_table('searches')

		self.static_image_folder = 'app/static/img/pages'
		self.static_thumbnail_folder = 'app/static/img/thumbnails'
		self.static_image_uri = 'static/img/pages'
		self.static_thumbnail_uri = 'static/img/thumbnails'


	def run(self, import_dir):
		image_extensions = ['.jpg', '.jpeg', '.png']

		for root, dirs, files in os.walk(import_dir):
			for file in files:
			# Check if the file has an image extension
				if any(file.lower().endswith(ext) for ext in image_extensions):

					# Get the file names and details
					image_file_extension = self.get_image_file_extension(file)
					raw_input_file = os.path.join(root, file)
					md5_file = self.calculate_md5(os.path.join(root,file))
					thumbnail_file = self.static_thumbnail_folder + '/' + md5_file + '.' + image_file_extension
					output_file = self.static_image_folder + '/' + md5_file + '.' + image_file_extension

					# The URI differs from the file path in that it is "/static/img/blah" and not "/app/static/img..."
					thumbnail_uri = self.static_thumbnail_uri + '/' + md5_file + '.' + image_file_extension
					output_uri = self.static_image_uri + '/' + md5_file + '.' + image_file_extension

					# Rotate the final printing images to fit portrait mode
					self.rotate_image(raw_input_file, output_file)

					# Scale the main printing image to a common max height
					image_size = self.create_scaled_image(output_file, output_file, self.image_height)

					# Don't rotate the thumbnails, merely scale them to all the same height
					thumbnail_size = self.create_scaled_image(raw_input_file, thumbnail_file, self.thumbnail_height)

					# Extract the Keywords described in the file
					keywords = self.get_keywords(raw_input_file)

					# Only update the image database if the -u or --update flag is set
					if self.update:
						self.update_database_image(md5_file, output_uri, image_size[0], image_size[1], thumbnail_uri, thumbnail_size[0], thumbnail_size[1])
						self.update_datebase_keywords(md5_file, keywords)

	def clean_database_table(self, table_name):
		connection = None
		try:
			# Connect to the SQLite database
			connection = sqlite3.connect(self.database_path)
			cursor = connection.cursor()
			cursor.execute(f'DELETE FROM {table_name};')
			# Commit the changes
			connection.commit()
			print(f"All data deleted from the '{table_name}' table.")
		except sqlite3.Error as e:
			print(f"Database Error: {e}")
		finally:
			# Close the connection
			if connection:
				connection.close()

	def update_database_image(self, md5_hash, image_path, image_width, image_height, thumbnail_path, thumbnail_width, thumbnail_height):
		connection = None
		try:
			# Connect to the SQLite database
			connection = sqlite3.connect(self.database_path)
			cursor = connection.cursor()
			created_at = int(datetime.datetime.now().date().strftime('%Y%m%d'))
			insert_query  = (f"INSERT INTO images ")
			insert_query += (f"(md5_hash, file_path, width, height, thumbnail_path, ")
			insert_query += (f"thumbnail_width, thumbnail_height, last_selected_yyyymmdd, total_selections) ")
			insert_query += (f"VALUES ('{md5_hash}','{image_path}', {image_width}, {image_height}, ")
			insert_query += (f"'{thumbnail_path}', {thumbnail_width}, {thumbnail_height}, {created_at}, 0);")
			cursor.execute(insert_query)
			connection.commit()
		except sqlite3.Error as e:
			print(f"Database Error: {e}")
		finally:
			# Close the connection
			if connection:
				connection.close()

	def update_datebase_keywords(self, md5_hash, keywords):
		connection = None
		insert_query = None
		try:
			connection = sqlite3.connect(self.database_path)
			cursor = connection.cursor()
			cursor.execute(f"SELECT id FROM images WHERE md5_hash='{md5_hash}';")
			image_id = cursor.fetchall()[0][0]
			for keyword in keywords:
				insert_query =  ("INSERT INTO keywords (image_id, keyword) VALUES (")
				insert_query += (f"{image_id}, '{keyword}');")
				cursor.execute(insert_query)
				connection.commit()
		except sqlite3.Error as e:
			print(f"Database Error: {e}, {insert_query}")
		finally:
			# Close the connection
			if connection:
				connection.close()

	def get_keywords(self, raw_input_file):
		all_keywords = raw_input_file.lower().split('/')[-1].split('.')[0].replace("_", " ").split()
		filtered_keywords = [s for s in all_keywords if not s.isdigit()]
		return filtered_keywords

	def get_image_file_extension(self, file_path):
		""" Returns the file extension at the tail end of 
		    the input path provided, e.g., .jpg, .png, .gif etc.
		"""
		extension = file_path.lower().split('.')[-1]
		return extension

	def calculate_md5(self, file_path):
		md5_hash = hashlib.md5()
		with open(file_path, "rb") as file:
			# Read the file in chunks for memory efficiency
			for chunk in iter(lambda: file.read(4096), b""):
				md5_hash.update(chunk)
		return md5_hash.hexdigest()

	def rotate_image(self, input_path, output_path):
		with Image.open(input_path) as img:
			width = img.size[0]
			height = img.size[1]
			if height < width:
				rotated_img = img.rotate(-90, expand=True)
				rotated_img.save(output_path)
			else:
				img.save(output_path)

	def create_scaled_image(self, input_path, output_path, target_height):
		"""
		Create a scaled image with a specified height while maintaining the aspect ratio.

		Parameters:
		- input_path: The path to the input image.
		- output_path: The path to save the scaled image.
		- target_height: The desired height for the scaled image.
		"""
		try:
			with Image.open(input_path) as img:
				# Calculate the width to maintain the aspect ratio
				aspect_ratio = img.width / img.height
				target_width = round(target_height * aspect_ratio)

				# Resize the image
				img = img.resize((target_width, target_height))

				# Save the scaled image
				img.save(output_path)

				# Return the image size
				return img.size
		except Exception as e:
			print(f"Error: {e}")
			exit(1)


def main(argv):
	parser = OptionParser(usage="Usage: import_images [-u|--update] <src-image-folder>")

	parser.add_option("-u", "--update",
		action="store_true",
		dest="updateFlag",
		default=False,
		help="Update database")

	(options, filename) = parser.parse_args()
	if len(filename) == 1:
		if os.path.exists(filename[0]) and os.path.isdir(filename[0]):
			importer = ImportImages(options.updateFlag)
			importer.run(filename[0])
		else:
			parser.print_help()
			print ('\nYou need to provide an input image folder.')
			exit(1)
	else:
		parser.print_help()
		print ('\nYou need to provide an input image folder.')
		exit(1)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
