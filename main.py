import os
import pdfplumber

def extract_specific_area_from_pdf(pdf_path, region):
    """
    Extract text from a specific region of each page of a PDF file.
    """
    with pdfplumber.open(pdf_path) as pdf:
        # Extract text from the specified region of each page
        text_per_page = [page.crop(region).extract_text() for page in pdf.pages]
    return text_per_page

def process_pdfs(input_folder, output_file, region):
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
                text_per_page = extract_specific_area_from_pdf(pdf_path, region)
                
                # Write the extracted text to the output file
                output_file.write(f"=== {filename} ===\n")
                for page_num, text in enumerate(text_per_page, start=1):
                    output_file.write(f"Page {page_num}:\n{text}\n\n")

# Specify input folder, output file, and the region to extract
input_folder = 'input'
output_file = 'output.txt'
# Specify the region to extract (replace with appropriate coordinates)
# For example: (x0, y0, x1, y1) where (x0, y0) is the top-left corner and (x1, y1) is the bottom-right corner
region = (75, 0, 500, 250)

# Process PDFs, delete existing output file, create a new one, and write parsed data to the new output file
process_pdfs(input_folder, output_file, region)
