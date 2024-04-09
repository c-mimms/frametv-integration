from samsungtvws import SamsungTVWS
import logging
import sys

#Delete if not necessary
sys.path.append('../')
ip = '192.168.1.19'

def get_active_image() -> str:
    # Get the active image
    tv = SamsungTVWS(ip)
    active_image = tv.art().get_current()
    logging.info(active_image)

    return active_image

def upload_image(file_path: str) -> str:
    # Upload image to FrameTV
    tv = SamsungTVWS(ip)

    with open(file_path, 'rb') as file:
        data = file.read()

    name = tv.art().upload(data, matte="none")
    
    logging.info(name)

    return name

def delete_image(name: str) -> None:
    # Delete an image from FrameTV
    tv = SamsungTVWS(ip)
    tv.art().delete(name)

def select_image(name: str) -> None:
    # Select the image to display
    tv = SamsungTVWS(ip)
    tv.art().select_image(name)