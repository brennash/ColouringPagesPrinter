import cups

def print_image(image_path, printer_name):
    """
    Print an image to a specified printer.

    Parameters:
    - image_path: The path to the image file.
    - printer_name: The name of the printer.

    Example:
    print_image("path/to/your/image.jpg", "Your_Printer_Name")
    """
    conn = cups.Connection()
    
    # Get the printer information
    printers = conn.getPrinters()
    
    # Check if the specified printer exists
    if printer_name not in printers:
        print(f"Error: Printer '{printer_name}' not found.")
        return
    
    # Get the default printer options
    printer_options = conn.getPrinterAttributes(printer_name)

    # Set print options (you may need to adjust these based on your printer)
    options = {
        'media': printer_options['media-default'],
        'fit-to-page': True,
    }

    # Print the image
    job_id = conn.printFile(
        printer_name, 
        image_path, 
        "Print Job", 
        options
    )

    print(f"Print job sent successfully. Job ID: {job_id}")

# Example usage
image_path = "path/to/your/image.jpg"
printer_name = "Your_Printer_Name"

print_image(image_path, printer_name)
