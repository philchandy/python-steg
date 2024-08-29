from PIL import Image, ImageChops, ImageEnhance
from stegano import lsb
import os
import numpy as np

#Program using stegano for steganography 


def convert_to_png(jpg_path, png_path):
    # Open the JPEG image
    with Image.open(jpg_path) as img:
        # Convert and save the image as PNG
        img.save(png_path, 'PNG')
        print(f"Image saved as: {png_path}")

def hide_file_in_image(image_path, file_path, output_image_path):
    # Read the content of the file to hide
    with open(file_path, 'rb') as file:
        file_data = file.read()

    # Convert file data to string to embed it in the image
    file_data_str = file_data.hex()

    # Use LSB to hide the data inside the image
    secret_image = lsb.hide(image_path, file_data_str)
    secret_image.save(output_image_path)

    print(f"File hidden successfully. Output image saved at: {output_image_path}")

def reveal_file_from_image(stego_image_path, output_file_path):
    # Extract the hidden data from the image
    hidden_data = lsb.reveal(stego_image_path)

    if hidden_data is None:
        print("No hidden data found.")
        return

    # Convert the string data back to bytes
    hidden_data_bytes = bytes.fromhex(hidden_data)

    # Save the extracted data to a file
    with open(output_file_path, 'wb') as output_file:
        output_file.write(hidden_data_bytes)

    print(f"Hidden file extracted successfully. Output file saved at: {output_file_path}")

def show_image_difference(original_path, converted_path, diff_path, scale_factor=10):
    # Open the original and converted images
    original = Image.open(original_path).convert('RGB')
    converted = Image.open(converted_path).convert('RGB')
    
    # Compute the difference
    difference = ImageChops.difference(original, converted)

    enhanced_diff = ImageEnhance.Brightness(difference).enhance(scale_factor)
    
    # Save or display the difference image
    enhanced_diff.save(diff_path)
    enhanced_diff.show()
    print(f"Difference image saved as: {diff_path}")


# Example usage
# convert_to_png('image.jpg', 'image.png')
image_path = 'image.png'  # Path to the input image
file_path = 'text.txt'        # Path to the file to hide
output_image_path = 'output_image.png'  # Path to save the output image
diff_path = 'difference_image.png'

# Hide the file
hide_file_in_image(image_path, file_path, output_image_path)

# Reveal the file
stego_image_path = 'output_image.png'   # Path to the stego image
extracted_file_path = 'extracted_secret.txt'  # Path to save the extracted file

reveal_file_from_image(stego_image_path, extracted_file_path)

show_image_difference(image_path, output_image_path, diff_path)