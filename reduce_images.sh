#!/bin/bash

# Directory containing the original images
input_dir="/static/img/main"

# Directory where the resized images will be stored
output_dir="/static/img/thumbs"

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Iterate over png files in the input directory
for img in $input_dir/*.png
do
  # Get the filename without path
  filename=$(basename -- "$img")

  # Resize and save to the output directory
  convert "$img" -resize 400x400^ "$output_dir/$filename"
done
