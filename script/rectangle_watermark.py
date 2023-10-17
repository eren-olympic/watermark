import os
import re
import csv
from PIL import Image, ImageOps
import sys
from tqdm import tqdm

watermark_path = sys.argv[1]
target_folder = sys.argv[2]
output_folder = sys.argv[3]

os.makedirs(output_folder, exist_ok=True)

watermark = Image.open(watermark_path)
filename_pattern = re.compile(r'^P\d{13}_(1|2|3|4)_.*\.(jpeg|jpg|png|JPG)$')

csv_file_path = os.path.join(os.path.dirname(watermark_path), 'output_status.csv')
csv_file = open(csv_file_path, mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['file_name', 'size', 'status'])

def add_watermark(watermark, target_image_path, output_image_path):
    filename = os.path.basename(target_image_path)
    
    try:
        target_image = Image.open(target_image_path)
    except IOError:
        print(f'Could not open {filename} as an image. Skipping this file.')
        csv_writer.writerow([filename, 'N/A', 'no'])
        return

    # Calculate padding
    max_side = max(target_image.width, target_image.height)
    left_padding = (max_side - target_image.width) // 2
    right_padding = max_side - target_image.width - left_padding
    top_padding = (max_side - target_image.height) // 2
    bottom_padding = max_side - target_image.height - top_padding
    
    # Create a new square image with white padding
    square_image = ImageOps.expand(target_image, (left_padding, top_padding, right_padding, bottom_padding), fill="white")

    # Apply watermark as previously
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
        if filename_pattern.match(filename):
            target_image_path = os.path.join(foldername, filename)
            relative_path = os.path.relpath(foldername, target_folder)
            output_image_folder = os.path.join(output_folder, relative_path)
            os.makedirs(output_image_folder, exist_ok=True)
            output_image_path = os.path.join(output_image_folder, filename)
            add_watermark(watermark, target_image_path, output_image_path)
        else:
            print(f'{filename} does not match the pattern. Skipping this file.')
            csv_writer.writerow([filename, 'N/A', 'no'])

csv_file.close()
