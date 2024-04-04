#!/usr/bin/env python
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO
import sys
import logging
from samsungtvws import SamsungTVWS

sys.path.append('../')

# # Increase debug level
logging.basicConfig(level=logging.DEBUG)

load_dotenv()
# gets OPENAI_API_KEY from your environment variables
openai = OpenAI()

def generate_image(prompt: str, model: str = "dall-e-3") -> Image:
    # Generate an image based on the prompt
    response = openai.images.generate(size="1792x1024", prompt=prompt, model=model)
    
    # Download the image from the URL
    image = requests.get(response.data[0].url)
    img = Image.open(BytesIO(image.content))

    return img

def resize_image(img: Image, new_width: int = 3840) -> Image:
    # Calculate aspect ratio
    original_width, original_height = img.size
    aspect_ratio = original_width / original_height

    # Calculate new dimensions, keeping aspect ratio
    new_height = int(new_width / aspect_ratio)

    # Resize the image
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Define the dimensions for cropping
    crop_height = 2160
    left = 0
    top = new_height - crop_height
    right = 3840
    bottom = new_height

    # Crop the image
    img_cropped = img.crop((left, top, right, bottom))

    return img_cropped

def main() -> None:
    # Generate an image based on the prompt
    prompt = """
    Apollo:
    A majestic 3-year-old Siberian Husky with a strikingly beautiful coat of black and white. His deep, ocean-blue eyes are filled with wisdom and tranquility. Apollo is a picture of grace and strength, embodying the spirit of the wild with his noble demeanor. He carries an air of mystery and adventure about him, as if he has many tales to tell from his journeys through the snow-covered forests of Siberia.
    Astro:
    An energetic 6-month-old Brittany Spaniel/Great Pyrenees mix puppy. Astro's coat is adorned with buff-colored spots, and freckles scatter playfully across his face and legs, giving him a uniquely endearing appearance. His almond-shaped eyes sparkle with curiosity and wonder, reflecting the boundless enthusiasm of youth. Astro is a bundle of joy and exuberance, always ready for adventure and eager to share his infectious zest for life with those around him."
    An illustration of Apollo and Astro frolicking by a frozen lake in the middle of a Swedish winter.
    """
    img = generate_image(prompt)
    img = resize_image(img)

    # Save the resized / cropped image
    img.save("image_cropped.png")

    # Upload image to FrameTV and set as current art
    tv = SamsungTVWS('192.168.1.21')

    with open(file_path, 'rb') as file:
        data = file.read()

    name = tv.art().upload(data, matte="none")
    logging.info(name)

    tv.art().select_image(name)

if __name__ == "__main__":
    main()