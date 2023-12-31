from PIL import Image
import random
import time
import cups
import os

class Printer:

	def __init__(self, verbose_flag=False):
		self.verbose = verbose_flag

	def print_image(self, image_path):
		job_id = None
		try:
			conn = cups.Connection()
			image_path_bytes = image_path.encode('utf-8')
			printers = conn.getPrinters()
			if not printers:
				if self.verbose:
					print(f"No printers found!!")
				return "No printers found"

			printer_name = list(printers.keys())[0]
			printer_name_bytes = printer_name.encode('utf-8')
			print_options = {'copies': 1, 'media': 'A4'}

			if self.verbose:
				print(f"Connecting to printer: {printer_name}")

			random_job_id = self.get_random_id()
			job_title = (f'Image_Print_Job_{random_job_id}')
			job_title_bytes = job_title.encode('utf-8')
			job_id = conn.createJob(printer_name, job_title, {})
			job_id_bytes = str(job_id).encode('utf-8')

			abs_path = str(os.getcwd()) + '/app/' + image_path
			abs_path_bytes = abs_path.encode('utf-8')

			if not os.path.isfile(abs_path):
				print(f"ERROR - {os.getcwd()}")
				print(f"ERROR - cannot find file to print {abs_path}")

			with open(abs_path, 'rb') as image_file:
				conn.printFile(printer_name_bytes, abs_path_bytes, job_id, options={})
			time.sleep(5)
			return "Printing..."
		except Exception as err:
			print(f"Error printing image {err}")
			return str(err)
		finally:
			job = conn.getJobAttributes(job_id)
			print(job)
			print(job['job-state'])
			if job['job-state'] == 9:
				print("Job Completed")
				conn.cancelJob("printer_name", job_id)
			else:
				print("Job is still in progress.")
				conn.cancelJob(job_id)

	def get_random_id(self):
		min = 0
		max = 999
		digits = [str(random.randint(min, max)) for i in range(5)]
		digits = [(len(str(max))-len(digit))*'0'+digit for digit in digits]
		return digits
