from rembg import remove
from PIL import Image
import os

def remove_background(input_path, output_path):
    try:
        with open(input_path, 'rb') as input_file:
            input_image = input_file.read()
        
        output_image = remove(input_image)
        
        with open(output_path, 'wb') as output_file:
            output_file.write(output_image)
        
        print(f"Background removed and image saved as: {output_path}")
    
    except Exception as e:
        print(f"Error: {str(e)}")

input_image = "input.png"
output_image = "output.png"

if os.path.exists(input_image):
    remove_background(input_image, output_image)
else:
    print(f"Input file {input_image} not found!")
