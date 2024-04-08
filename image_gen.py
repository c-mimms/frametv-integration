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
    img = Image.new('RGBA', (3840, 2160), color = (255, 255, 255, 125))

    d = ImageDraw.Draw(img)

    # Starting position of the message
    border = 20
    x = border * 2
    y = border
    font_path = '/Library/Fonts/Noteworthy.ttc'
    font_size = 80
    day_font_size = 90
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
        d.text((x, y), day_name, font=day_font, fill=(0, 0, 0, 255))
        for event in events:
        # Check if the event start is a date or datetime
            y += event_spacing * font_size
            if isinstance(event.start, datetime):
                event_text = f"    {event.start.strftime('%-I:%M %p')} - {event.summary}"
                fill_color = (90, 90, 90, 255)
            else:
                event_text = f"  {event.summary}"

            fill_color = (60, 60, 155, 255)
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
    img = Image.new('RGBA', (500, 2000), color = (255, 255, 255, 0))
    d = ImageDraw.Draw(img)

    # Starting position of the message
    x = 10
    y = 10
    
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
        max_width = max(max_width, d.textlength(day['day'], font=fnt))
        max_height = max(max_height, y)

        # Add spacing between days
        y += day_space
    
    # Crop the image to fit the size of the text
    img = img.crop((0, 0, max_width + 2 * x, max_height))

    # Save the image
    img.save('images/forecast.png', "PNG")

def main() -> None:

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

    # Generate an image based on the prompt
    prompt = """Apollo:
Apollo is a lovable yellow lab mix with a light orangish coat that radiates warmth and charm. His gentle face shows traces of wisdom and a hint of gray, a testament to the experiences he's shared with his family. With a wagging tail and a heart full of kindness, Apollo is the epitome of a faithful and caring canine companion.

Astro:
An energetic 6-month-old Brittany Spaniel/Great Pyrenees mix 8 month old young dog. Astro's coat is adorned with buff-colored spots, and freckles scatter playfully across his face and legs, giving him a uniquely endearing appearance. His almond-shaped eyes sparkle with curiosity and wonder, reflecting the boundless enthusiasm of youth. Astro is a bundle of joy and exuberance, always ready for adventure and eager to share his infectious zest for life with those around him."
An image of Apollo and Astro as they are staring off into the distance of the Scottish highlands. The weather is {weather}. The dogs are facing away from the viewer, sitting on the left side of the image and looking towards the distance. The right part the image showcases the beautiful landscape stretching out in front of them.
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

    # Get 3 day schedule from google calendar
    events = get_events_for_next_days(days=3)
    create_image_with_text(events)

    image1 = Image.open('images/image_cropped.png').convert("RGBA")
    image2 = Image.open('images/event_list.png').convert("RGBA")
    image3 = Image.open('images/forecast.png').convert("RGBA")

    # Calculate the position of the top right corner of the second image and overlay weather
    position = (image1.width - image3.width, 0)
    image1.paste(image3, position, image3)

    # Same for events in bottom right
    position = (image1.width - image2.width, image1.height - image2.height)
    image1.paste(image2, position, image2)

    # Save the result
    image1.save('images/overlay.png', 'PNG')

    name = art.upload_image("images/overlay.png")
    art.select_image(name)

if __name__ == "__main__":
    main()