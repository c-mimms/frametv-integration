#!/usr/bin/env python
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import logging
import os
from datetime import datetime, timedelta
import argparse

# Local imports
import art
import weather
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
    img = Image.new('RGBA', (3840, 2160), color = (0, 0, 0, 50))

    d = ImageDraw.Draw(img)

    # Starting position of the message
    border = 20
    x = border * 2
    y = border
    font_path = '/Library/Fonts/Noteworthy.ttc'
    font_size = 50
    day_font_size = 60
    event_spacing = 1.5
    day_spacing = 2.5

    # Load a TrueType or OpenType font file, and create a font object.
    # This step depends on the font file you have and the size of text you want
    fnt = ImageFont.truetype(font_path, font_size, 1)
    day_font = ImageFont.truetype(font_path, day_font_size, 1)

    # Keep track of the maximum width and height
    max_width = 0
    max_height = 0

    # Group events by day
    events_by_day = {}
    for event in events:
        logging.info(event)
        if isinstance(event.start, datetime):
            day = event.start.date()
        else:
            day = event.start
        if day not in events_by_day:
            events_by_day[day] = []
        events_by_day[day].append(event)

    # Ensure only 3 days are displayed
    events_by_day = dict(sorted(events_by_day.items())[:3])

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
        d.text((x, y), day_name, font=day_font, fill=(255, 255, 255, 255))
        for event in events:
        # Check if the event start is a date or datetime
            y += event_spacing * font_size
            if isinstance(event.start, datetime):
                event_text = f"    {event.start.strftime('%-I:%M %p')} - {event.summary}"
                fill_color = (90, 90, 90, 255)
            else:
                event_text = f"  {event.summary}"

            # fill_color = (160, 160, 255, 255)
            fill_color = (0, 0, 0, 255)
            d.text((x, y), event_text, font=fnt, fill=fill_color)
            
            event_width = d.textlength(event_text, font=fnt)
            max_width = max(max_width, event_width)
        
        y += day_spacing * font_size
        # Update the maximum height
        max_height = max(max_height, y)

    # Crop the image to fit the size of the text
    img = img.crop((0, 0, max_width + 2 * border, max_height + border))

    # Save the image
    img.save('images/event_list.png', "PNG")

def create_forecast_image(forecast):
    # Image should be a narrow vertical strip with the highs and lows for the next 3 days and the weather icons
    img = Image.new('RGBA', (500, 2000), color = (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Starting position of the message
    border = 20
    x = border
    y = border
    
    font_path = '/Library/Fonts/Noteworthy.ttc'
    font_size = 60
    icon_size = 160
    small_font_size = 30
    small_space = 100
    spacing = 60
    day_space = 40
    padding = 40
    
    # Load a TrueType or OpenType font file, and create a font object.
    fnt = ImageFont.truetype(font_path, font_size, 1)
    fnt2 = ImageFont.truetype(font_path, small_font_size, 1)
    emoji_fnt = ImageFont.truetype('/System/Library/Fonts/Apple Color Emoji.ttc', icon_size)

    # Keep track of the maximum width and height
    max_width = 0
    max_height = 0

    for day in forecast:
        # Print the day formatted like "Monday"
        #parse date from string to get day of the week
        day_date = datetime.strptime(day['day'], '%Y-%m-%d')
        day_word = day_date.strftime('%A')
        d.text((x, y), day_word, font=fnt, fill=(255, 255, 255, 255))

        y += font_size + padding
        # d.line((x, y, x + icon_size, y), fill=(255, 255, 255, 255), width=2)
        
        weather_code = day['weather_code']
        if weather_code in [0]:
            icon = "☀️"
        elif weather_code in [1]:
            icon = "🌤️"
        elif weather_code in [2]:
            icon = "⛅"
        elif weather_code in [3]:
            icon = "🌥️"
        elif weather_code in [45, 48]:
            icon = "🌫️"
        elif weather_code in [51, 53, 55]:
            icon = "🌧️"
        elif weather_code in [56, 57]:
            icon = "❄️"
        elif weather_code in [61, 63, 65]:
            icon = "🌧️"
        elif weather_code in [66, 67]:
            icon = "❄️"
        elif weather_code in [71, 73, 75]:
            icon = "🌨️"
        elif weather_code == 77:
            icon = "❄️"
        elif weather_code in [80, 81, 82]:
            icon = "🌦️"
        elif weather_code in [85, 86]:
            icon = "🌨️"
        elif weather_code == 95:
            icon = "⛈️"
        else:
            print(f"Unknown weather code: {weather_code}")
            icon = "❓"
        
        #Horizontal line
        # d.line((x, y, x, y + icon_size), fill=(255, 255, 255, 255), width=2)
        #Emoji for forecast
        d.text((x, y), icon, font=emoji_fnt, embedded_color=True, anchor="la")

        # Print the high and low temperatures to the right of the icon
        temp_text = f"{round(day['max_temp'])}°F"
        d.text((x + icon_size + small_space, y + padding ), temp_text, font=fnt2, anchor="ra", fill=(255, 255, 255, 255))
        temp_text = f"{round(day['min_temp'])}°F"
        d.text((x + icon_size + small_space, y + small_space), temp_text, font=fnt2, anchor="ra", fill=(255, 255, 255, 255))
        y += icon_size

        # Update the maximum width and height
        max_width = max(max_width, d.textlength(day_word, font=fnt))
        max_height = max(max_height, y)

        # Add spacing between days
        y += day_space
    
    # Crop the image to fit the size of the text
    img = img.crop((0, 0, max_width + 2 * border, max_height + border))

    # Save the image
    img.save('images/forecast.png', "PNG")

def main() -> None:
    # Create the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--background-image', type=str, help='Path to the background image')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Parse the command-line arguments
    args = parser.parse_args()


    # # Increase debug level
    logging.basicConfig(level=logging.INFO)

    # Get the weather forecast for the next 3 days
    forecast = weather.get_forecast()

    # Create an image with the weather forecast
    create_forecast_image(forecast)

    # return
    # Get todays weather from forecast
    today = forecast[0]
    weather_code = today['weather_code']
    if weather_code in [0]:
        weather_text = "sunny"
    elif weather_code in [1, 2]:
        weather_text = "partly cloudy"
    elif weather_code in [3]:
        weather_text = "overcast"
    elif weather_code in [45, 48]:
        weather_text = "foggy"
    elif weather_code in [51, 53, 55]:
        weather_text = "drizzly"
    elif weather_code in [56, 57]:
        weather_text = "freezing drizzle"
    elif weather_code in [61, 63, 65]:
        weather_text = "rain"
    elif weather_code in [66, 67]:
        weather_text = "freezing rain"
    elif weather_code in [71, 73, 75]:
        weather_text = "snow"
    elif weather_code == 77:
        weather_text = "snow grains"
    elif weather_code in [80, 81, 82]:
        weather_text = "rain showers"
    elif weather_code in [85, 86]:
        weather_text = "snow showers"
    elif weather_code == 95:
        weather_text = "thunderstorm"


    if not args.background_image:
        # Generate an image based on the prompt
        prompt = """Apollo is a lovable yellow lab mix with a light orangish coat that radiates warmth and charm. His gentle face shows traces of wisdom and a hint of gray, a testament to the experiences he's shared with his family. With a wagging tail and a heart full of kindness, Apollo is the epitome of a faithful and caring canine companion.
    Astro is an energetic 8-month-old Brittany Spaniel/Great Pyrenees mix young dog. Astro's coat is adorned with buff-colored spots, and freckles scatter playfully across his face and legs, giving him a uniquely endearing appearance. His almond-shaped eyes sparkle with curiosity and wonder, reflecting the boundless enthusiasm of youth. Astro is a bundle of joy and exuberance, always ready for adventure and eager to share his infectious zest for life with those around him."
    In a scene that fills the entire frame with no perimeter, Apollo and Astro sit staring off into the distance of the Scottish highlands. The weather is {weather}. The eautiful landscape stretches out in front of them.
    """
        img = generate_image(prompt.format(weather=weather_text))

        # Find a filename that doesn't exist and save the generated image
        i = 1
        while os.path.exists(f"images/image_gen_{i}.png"):
            i += 1
        img.save(f"images/image_gen_{i}.png")

        img = resize_image(img)

        # Save the resized / cropped image
        img.save("images/image_cropped.png")
    
    else:
        img = Image.open(args.background_image)
        img = resize_image(img)
        img.save("images/image_cropped.png")

    # Get 3 day schedule from google calendar
    events = get_events_for_next_days(days=3)
    create_image_with_text(events)

    image1 = Image.open('images/image_cropped.png').convert("RGBA")
    image2 = Image.open('images/event_list.png').convert("RGBA")
    image3 = Image.open('images/forecast.png').convert("RGBA")

    # Calculate the position of the top right corner of the second image and overlay weather
    position = (image1.width - image3.width, 0)
    # Draw a transparent black rounded rectangle where the weather will be displayed
    rectangle = Image.new('RGBA', image3.size)
    draw = ImageDraw.Draw(rectangle, "RGBA")
    draw.rounded_rectangle([0, 0, rectangle.width, rectangle.height], fill=(0, 0, 0, 50), outline=None, width=0, radius=30)

    image1.paste(rectangle, position, rectangle)
    image1.paste(image3, position, image3)

    # Same for events in bottom right
    position = (image1.width - image2.width, image1.height - image2.height)
    image1.paste(image2, position, image2)

    # Save the result
    image1.save('images/overlay.png', 'PNG')


    # Upload the image to the FrameTV

    active_image = art.get_active_image()
    # {'id': 'd979b04f-8911-4738-95d1-eb4b43a4e735', 'event': 'current_artwork', 'content_id': 'SAM-F0103', 'matte_id': 'none', 'portrait_matte_id': 'flexible_polar', 'target_client_id': 'e567129a-d767-4e3-924d-e2373485431b'}
    # Parse out content_id
    content_id = active_image['content_id']

    # Check images/image_name.txt for previous image name
    previous_images = []
    try:
        with open('images/image_name.txt', 'r') as f:
            for line in f:
                previous_images.append(line.strip())  
    except FileNotFoundError:
        pass

    name = art.upload_image("images/overlay.png")
    print(name)
    with open('images/image_name.txt', 'a') as f:
        f.write(name + '\n')
    art.select_image(name)

    # Delete previous active image if it matched a previous image
    if content_id in previous_images:
        print(f"Deleting previous image {content_id}")
        art.delete_image(content_id)

if __name__ == "__main__":
    main()