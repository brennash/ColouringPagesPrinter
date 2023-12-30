class Thumbnail:

	def __init__(self, md5_key):
		self.md5_key = md5_key
		self.file_path = None
		self.thumbnail_path = None

	def get_md5_hash(self):
		return self.md5_key

	def set_file_path(self, file_path):
		self.file_path = file_path

	def get_file_path(self):
		return self.file_path 

	def set_thumbnail_path(self, thumbnail_path):
		self.thumbnail_path = thumbnail_path

	def get_thumbnail_path(self):
		return self.thumbnail_path 
