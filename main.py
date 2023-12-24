import os
import pdfplumber

def extract_specific_area_from_pdf(pdf_path, sq_coords, address_coords, type_coords, po_coords, total_coords):
    """
    Extract text from a specific region of each page of a PDF file.
    """
    with pdfplumber.open(pdf_path) as pdf:
        # Extract text from the specified region of each page
        sq_text = [page.crop(sq_coords).extract_text() for page in pdf.pages]
        address_text = [page.crop(address_coords).extract_text() for page in pdf.pages]
        type_text = [page.crop(type_coords).extract_text() for page in pdf.pages]
        po_text = [page.crop(po_coords).extract_text() for page in pdf.pages]
        total_text = [page.crop(total_coords).extract_text() for page in pdf.pages]
    return sq_text, address_text, type_text, po_text, total_text

def process_pdfs(input_folder, output_file, sq_coords, address_coords, type_coords, po_coords, total_coords):
    """
    Process all PDFs in the input folder, delete existing output file,
    create a new one, and write parsed data to the new output text file.
    """
    # Check if the output file exists and delete it
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # Open the new output file in write mode
    with open(output_file, 'w', encoding='utf-8') as output_file:
        # Iterate through all files in the input folder
        for filename in os.listdir(input_folder):
            if filename.endswith('.pdf'):
                pdf_path = os.path.join(input_folder, filename)
                
                # Extract text from the specified region of each page of the PDF
                sq_text, address_text, type_text, po_text, total_text = extract_specific_area_from_pdf(pdf_path, sq_coords, address_coords, type_coords, po_coords, total_coords)
                
                # Write the extracted text to the output file
                output_file.write(f"=== {filename} ===\n")
                for page_num, (sq, address, type, po, total) in enumerate(zip(sq_text, address_text, type_text, po_text, total_text), start=1):
                    output_file.write(f"Page {page_num}:\n")
                    output_file.write(f"{sq} {address} {type}\nPO# {po}\n${total}\n")
                    output_file.write("\n")

# Specify input folder, output file, and the region to extract
input_folder = 'input'
output_file = 'output.txt'
# Specify the region to extract (replace with appropriate coordinates)
# For example: (x0, y0, x1, y1) where (x0, y0) is the top-left corner and (x1, y1) is the bottom-right corner

# Good Cords
sq_coords = (428, 335, 461, 348)
# Bad Cords
address_coords = (399, 150, 545, 162)
# Good Cords
type_coords = (152, 336, 168, 345)
# Good Cords
po_coords = (502, 79, 541, 96)
# Good Cords
total_coords = (522, 355, 599, 373)

# Process PDFs, delete existing output file, create a new one, and write parsed data to the new output file
process_pdfs(input_folder, output_file, sq_coords, address_coords, type_coords, po_coords, total_coords)
