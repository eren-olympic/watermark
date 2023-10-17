import os
import csv
from PIL import Image, ImageOps
import sys
from tqdm import tqdm

# Get the watermark image, target folder, and output folder from the command line arguments
watermark_path = sys.argv[1]
target_folder = sys.argv[2]
output_folder = sys.argv[3]

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the watermark image
watermark = Image.open(watermark_path)

# Open the CSV file and create a set of filenames to be processed
csv_file_path = 'target.csv'
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    csv_reader = csv.DictReader(file)
    filenames_to_process = set(row['file_name'] for row in csv_reader if row['status'] == 'no')

# Initialize the CSV writer
output_csv_file_path = os.path.join(output_folder, 'output_status.csv')
output_csv_file = open(output_csv_file_path, mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(output_csv_file)
csv_writer.writerow(['file_name', 'size', 'status'])


def add_watermark(watermark, target_image_path, output_image_path):
    filename = os.path.basename(target_image_path)
    
    if not os.path.exists(target_image_path):
        print(f'{filename} does not exist. Skipping this file.')
        csv_writer.writerow([filename, 'N/A', 'file does not exist'])
        return
    
    try:
        target_image = Image.open(target_image_path)
    except IOError:
        print(f'Could not open {filename} as an image. Skipping this file.')
        csv_writer.writerow([filename, 'N/A', 'invalid image'])
        return
    
    max_side = max(target_image.width, target_image.height)
    left_padding = (max_side - target_image.width) // 2
    right_padding = max_side - target_image.width - left_padding
    top_padding = (max_side - target_image.height) // 2
    bottom_padding = max_side - target_image.height - top_padding

    square_image = ImageOps.expand(target_image, (left_padding, top_padding, right_padding, bottom_padding), fill="white")

    watermark_resized = watermark.resize(square_image.size)
    watermark_with_alpha = Image.new('RGBA', square_image.size)
    watermark_with_alpha.paste(watermark_resized, (0,0))

    if square_image.mode != 'RGBA':
        square_image = square_image.convert('RGBA')

    watermarked_image = Image.alpha_composite(square_image, watermark_with_alpha)
    watermarked_image = watermarked_image.convert('RGB')
    watermarked_image.save(output_image_path)
    csv_writer.writerow([filename, f'{square_image.width}*{square_image.height}', 'yes'])


for foldername, _, filenames in os.walk(target_folder):
    for filename in tqdm(filenames, desc="Processing images", unit="file"):
        # Check if the filename is in the list of filenames to process
        if filename in filenames_to_process:
            target_image_path = os.path.join(foldername, filename)
            output_image_folder = os.path.join(output_folder, os.path.relpath(foldername, target_folder))
            os.makedirs(output_image_folder, exist_ok=True)
            output_image_path = os.path.join(output_image_folder, filename)
            add_watermark(watermark, target_image_path, output_image_path)

output_csv_file.close()