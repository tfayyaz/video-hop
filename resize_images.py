from PIL import Image
import os

# Input directory containing the images
input_dir = "./static/img/main"

# Output directory where resized images will be stored
output_dir = "./static/img/thumbs"

# Create the output directory if it doesn't exist
# os.makedirs(output_dir, exist_ok=True)

# Iterate over png files in the input directory
for img_name in os.listdir(input_dir):
    if img_name.endswith(".png"):
        # Open an image file
        with Image.open(os.path.join(input_dir, img_name)) as img:
            # Calculate the width and height of a new image.
            width, height = img.size
            new_height = height
            new_width = width
            
            if width > height:
                new_width = 400
                new_height = int(new_width * height / width)
            else:
                new_height = 400
                new_width = int(new_height * width / height)

            # Resize the image
            img_resized = img.resize((new_width, new_height), Image.ANTIALIAS)
