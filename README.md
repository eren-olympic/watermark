<p align="center">
  <a href="./README.md">English</a> |
  <a href="./README-CN.md">繁體中文</a>
</p>

# Watermark Application README

This set of scripts allows you to apply watermarks to images in specified directories. Two different approaches are provided:

1. `filled_watermark.py` – Applies a watermark to images specified in a CSV file.
2. `rectangle_watermark.py` – Applies a watermark to images that match a specific filename pattern.

## Setup

1. Install Python (3.6 or later is recommended).
2. Install the required libraries using pip:
   ```bash
   pip install Pillow tqdm
   ```

## Usage

### `filled_watermark.py`

This script adds a watermark to images specified in `target.csv`. 

**Usage**:
```bash
python filled_watermark.py [WATERMARK_PATH] [TARGET_FOLDER] [OUTPUT_FOLDER]
```

**Arguments**:
- `WATERMARK_PATH`: Path to the watermark image.
- `TARGET_FOLDER`: Directory containing the images to be watermarked.
- `OUTPUT_FOLDER`: Directory where the watermarked images will be saved.

Before using this script, create a `target.csv` in the same directory with the following format:
```
file_name,status
image1.jpg,no
image2.jpg,yes
...
```

Images with a status of "no" will be processed.

The script will generate an `output_status.csv` in the `OUTPUT_FOLDER`, indicating the processing status for each image.

### `rectangle_watermark.py`

This script adds a watermark to images that match a specific filename pattern: `^P\d{13}_(1|2|3|4)_.*\.(jpeg|jpg|png|JPG)$`.

**Usage**:
```bash
python rectangle_watermark.py [WATERMARK_PATH] [TARGET_FOLDER] [OUTPUT_FOLDER]
```

**Arguments**:
- `WATERMARK_PATH`: Path to the watermark image.
- `TARGET_FOLDER`: Directory containing the images to be watermarked.
- `OUTPUT_FOLDER`: Directory where the watermarked images will be saved.

The script will generate an `output_status.csv` in the same directory as the watermark image, indicating the processing status for each image.

## Notes

- Both scripts will process images and make them square by adding white padding before applying the watermark.
- If any errors occur during processing, they will be logged in the `output_status.csv` file.

## Contributing

If you find any bugs or have suggestions, please open an issue or submit a pull request. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.