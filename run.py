import os
from PIL import Image, ImageDraw

# Define the size of the final Roll20 token
TOKEN_SIZE = 512  # Roll20 tokens are 512x512 pixels

def crop_to_circle(image):
    """
    Crop the input image to a circle.
    """
    width, height = image.size
    min_dim = min(width, height)

    # Create a mask with a circle
    mask = Image.new('L', (min_dim, min_dim), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, min_dim, min_dim), fill=255)

    # Center the image by cropping to the smallest dimension
    offset_x = (width - min_dim) // 2
    offset_y = (height - min_dim) // 2
    cropped_image = image.crop((offset_x, offset_y, offset_x + min_dim, offset_y + min_dim))

    # Apply the circular mask
    cropped_image.putalpha(mask)

    return cropped_image

def resize_image(image, size):
    """
    Resize the input image to the given size while maintaining the aspect ratio.
    """
    return image.resize((size, size), Image.Resampling.LANCZOS)

def overlay_border(token_image, border_image):
    """
    Overlay a fancy border onto the token image.
    Both images should be RGBA and of the same size.
    """
    border_resized = border_image.resize(token_image.size, Image.Resampling.LANCZOS)
    return Image.alpha_composite(token_image, border_resized)

def process_image(input_path, border_path, output_path):
    """
    Process a single image: crop it to a circle, resize it, apply the border, and save it.
    """
    image = Image.open(input_path).convert("RGBA")  # Ensure image is in RGBA mode for transparency
    border_image = Image.open(border_path).convert("RGBA")  # Ensure the border image is in RGBA mode

    # Crop image to a circle
    circular_image = crop_to_circle(image)

    # Resize the image to the token size
    resized_image = resize_image(circular_image, TOKEN_SIZE)

    # Overlay the fancy border
    token_with_border = overlay_border(resized_image, border_image)

    # Save the processed image
    token_with_border.save(output_path, format="PNG")

def process_images_in_folder(input_folder, border_path, output_folder):
    """
    Process all images in the input folder, apply circular cropping, resizing,
    and overlay a fancy border. Save the tokens in the output folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0].replace('-ori', '') + '_token.png'
            output_path = os.path.join(output_folder, output_filename)

            # Process each image
            process_image(input_path, border_path, output_path)
            print(f"Processed {filename} and saved as {output_filename}")

# Example usage
input_folder = 'input/'
border_path = 'border.png'  # Path to the fancy border image
output_folder = 'output/'
process_images_in_folder(input_folder, border_path, output_folder)
