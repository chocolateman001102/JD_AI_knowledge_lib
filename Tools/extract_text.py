import PyPDF2
import os

# Prompt the user to enter the path to a PDF file or a directory containing PDF files
path = input("Please enter the path to a PDF file or a directory containing PDF files: ")

try:
    if os.path.isfile(path) and path.endswith('.pdf'):
        # Single PDF file
        pdf_files = [path]
    elif os.path.isdir(path):
        # Directory containing PDF files
        files = os.listdir(path)
        pdf_files = [os.path.join(path, file) for file in files if file.endswith('.pdf')]
    else:
        print("The specified path is neither a PDF file nor a directory containing PDF files.")
        pdf_files = []

    if not pdf_files:
        print("No PDF files found.")
    else:
        for pdf_path in pdf_files:
            # Open the PDF file
            with open(pdf_path, 'rb') as file:
                # Create a PDF reader object
                reader = PyPDF2.PdfReader(file)
                
                # Initialize a variable to store the extracted text
                extracted_text = ''
                
                # Iterate through each page in the PDF
                for page_number, page in enumerate(reader.pages, start=1):
                    # Extract text from the page
                    text = page.extract_text()
                    if text:
                        extracted_text += text + '\n'
                    else:
                        print(f"Warning: No text extracted from page {page_number} in {os.path.basename(pdf_path)}")

            # Extract the file name without extension
            file_name = os.path.splitext(os.path.basename(pdf_path))[0]
            
            # Construct the output text file path
            output_txt_path = os.path.join(os.path.dirname(pdf_path), f"{file_name}.txt")
            
            # Write the extracted text to a text file
            with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(extracted_text)
            
            print(f"Extracted text from {os.path.basename(pdf_path)} has been saved to {output_txt_path}")

except FileNotFoundError:
    print(f"Error: The path {path} was not found.")
except Exception as e:
    print(f"An error occurred: {e}")