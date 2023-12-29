from PIL import Image
import cups
import os

# Create a connection to the CUPS server
conn = cups.Connection()

image_path = '/home/brennash/Software/ColouringPagesPrinter/imgs/peppa_pig_teddy_1.jpeg'
image_path_bytes = image_path.encode('utf-8')

# Get a list of available printers
printers = conn.getPrinters()

if not printers:
	print("No printers found.")
	exit(1)

# Choose the first printer in the list (you can modify this based on your needs)
printer_name = list(printers.keys())[0]
printer_name_bytes = printer_name.encode('utf-8')

print(f"Connecting to printer: {printer_name}")

# Get information about the selected printer
printer_info = conn.getPrinterAttributes(printer_name)

print(f"Printer Name: {printer_info['printer-info']}")
print(f"Printer Model: {printer_info['printer-make-and-model']}")
print(f"Printer State: {printer_info['printer-state']}")

print(f"Printer Name: {printer_name}")

print_options = {'copies': 1, 'media': 'A4'}

job_title = 'Flask_Job_1'
job_title_bytes = job_title.encode('utf-8')

job_id = conn.createJob(printer_name, "Flask_Job_1", {})
job_id_bytes = str(job_id).encode('utf-8')


with open(image_path, 'rb') as image_file:
	conn.printFile(printer_name_bytes, image_path_bytes, job_id_bytes, options={})
conn.closeJob(job_id)
