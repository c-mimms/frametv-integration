#!/usr/bin/env python
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import logging
import os
from datetime import datetime, timedelta

# Local imports
import art
from cal import get_events_for_next_days


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


def create_image_with_text(events):
    # Create a new image with white background
    img = Image.new('RGBA', (3840, 2160), color = (255, 255, 255, 125))

    d = ImageDraw.Draw(img)

    # Starting position of the message
    border = 20
    x = border * 2
    y = border
    font_path = '/Library/Fonts/Noteworthy.ttc'
    font_size = 80
    event_spacing = 1.5
    day_spacing = 2.5

    # Load a TrueType or OpenType font file, and create a font object.
    # This step depends on the font file you have and the size of text you want
    fnt = ImageFont.truetype(font_path, font_size, 1)

    # Keep track of the maximum width and height
    max_width = 0
    max_height = 0

    # Group events by day
    events_by_day = {}
    for event in events:
        day = event.start.date()
        if day not in events_by_day:
            events_by_day[day] = []
        events_by_day[day].append(event)

    # Print events grouped by day
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    for day, events in events_by_day.items():
        if day == today:
            day_name = "Today"
        elif day == tomorrow:
            day_name = "Tomorrow"
        else:
            day_name = day.strftime('%A')
        d.text((x, y), day_name, font=fnt, fill=(0, 0, 0, 255))
        for event in events:
            y += event_spacing * font_size
            event_text = f"    {event.start.strftime('%-I:%M %p')} - {event.summary}"
            d.text((x, y), event_text, font=fnt, fill=(0, 0, 0, 255))
            event_width = d.textlength(event_text, font=fnt)
            max_width = max(max_width, event_width)
        
        y += day_spacing * font_size
        # Update the maximum height
        max_height = max(max_height, y)

    # Crop the image to fit the size of the text
    img = img.crop((0, 0, max_width + 2 * border, max_height + border))

    # Save the image
    img.save('images/event_list.png', "PNG")

def main() -> None:

    # # Increase debug level
    logging.basicConfig(level=logging.INFO)

    # Generate an image based on the prompt
    prompt = """Apollo:
Apollo is a lovable yellow lab mix with a light orangish coat that radiates warmth and charm. His gentle face shows traces of wisdom and a hint of gray, a testament to the experiences he's shared with his family. With a wagging tail and a heart full of kindness, Apollo is the epitome of a faithful and caring canine companion.

Astro:
An energetic 6-month-old Brittany Spaniel/Great Pyrenees mix 8 month old young dog. Astro's coat is adorned with buff-colored spots, and freckles scatter playfully across his face and legs, giving him a uniquely endearing appearance. His almond-shaped eyes sparkle with curiosity and wonder, reflecting the boundless enthusiasm of youth. Astro is a bundle of joy and exuberance, always ready for adventure and eager to share his infectious zest for life with those around him."
An illustration of Apollo and Astro playing together in the Scottish highlands. The image is beautifully composed, with both dogs located in the left third of the image, drawing your eyes but not distracting from the beautiful landscape stretching out behind them.
"""
    img = generate_image(prompt)
    # Find a filename that doesn't exist and save the generated image
    i = 1
    while os.path.exists(f"images/image_gen_{i}.png"):
        i += 1
    img.save(f"images/image_gen_{i}.png")

    img = resize_image(img)

    # Save the resized / cropped image
    img.save("images/image_cropped.png")

    events = get_events_for_next_days(days=3)
    create_image_with_text(events)

    image1 = Image.open('images/image_cropped.png').convert("RGBA")
    image2 = Image.open('images/event_list.png').convert("RGBA")

    # Calculate the position of the top right corner of the second image
    position = (image1.width - image2.width, image1.height - image2.height)

    # Paste image2 onto image1
    image1.paste(image2, position, image2)

    # Save the result
    image1.save('images/overlay.png', 'PNG')

    name = art.upload_image("images/overlay.png")
    art.select_image(name)

if __name__ == "__main__":
    main()