from samsungtvws import SamsungTVWS
import logging
import sys

#Delete if not necessary
sys.path.append('../')
ip = '192.168.1.19'

def upload_image(file_path: str) -> str:
    # Upload image to FrameTV
    tv = SamsungTVWS(ip)

    with open(file_path, 'rb') as file:
        data = file.read()

    name = tv.art().upload(data, matte="none")
# # tv.art().delete('MY-F0020')
    
    logging.info(name)

    return name

def select_image(name: str) -> None:
    # Select the image to display
    tv = SamsungTVWS(ip)
    tv.art().select_image(name)