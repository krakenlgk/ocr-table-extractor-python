import cv2
import pytesseract
import numpy as np
import re

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'path_to_tesseract.exe'  # Update with your Tesseract installation path

# Load the image
image_path = 'kkr_summary.png'  # Update with the path to your image
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply some preprocessing to improve OCR accuracy
gray = cv2.medianBlur(gray, 3)

# Use thresholding to binarize the image
_, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Use PyTesseract to extract text
custom_config = r'--oem 3 --psm 6'  # OCR Engine Mode 3, Page Segmentation Mode 6
extracted_text = pytesseract.image_to_string(thresh, config=custom_config)

# Split the extracted text into lines
lines = extracted_text.split('\n')

# Function to identify table sections dynamically
def identify_table_sections(lines):
    sections = {}
    current_section = None
    for line in lines:
        if re.search(r'Run Rate|Dot Balls|Balls played/Wicket|% of balls converted into boundaries', line, re.I):
            current_section = line.strip()
            sections[current_section] = []
        elif current_section:
            if line.strip():
                sections[current_section].append(line.strip())
    return sections

# Extract sections from the lines
sections = identify_table_sections(lines)

# Helper function to print extracted tables
def print_extracted_tables(sections):
    for section, content in sections.items():
        print(f"\n{section} Table:")
        for line in content:
            print(line)

# Print the tables extracted from the image
print_extracted_tables(sections)