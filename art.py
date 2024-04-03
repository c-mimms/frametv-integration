from samsungtv import SamsungTV

# tv2 = SamsungTV('192.168.1.21', token='66308911')
# tv2.power()

import sys
import logging

sys.path.append('../')

from samsungtvws import SamsungTVWS

# # Increase debug level
logging.basicConfig(level=logging.INFO)

# # Normal constructor
tv = SamsungTVWS('192.168.1.21')

tv.art().select_image('MY_F0080')

# info = tv.art().get_device_info()
# logging.info(info)

# info = tv.art().get_api_version()
# logging.info(info)

# info = tv.art().available()
# logging.info(info)

# # Retrieve information about the currently selected art
# info = tv.art().get_current()
# logging.info(info)



# # # Is art mode supported?
# info = tv.art().supported()
# logging.info(info)
# # tv.shortcuts().power()

# # List the art available on the device
# info = tv.art().available()
# logging.info(info)

# # Retrieve information about the currently selected art
# info = tv.art().get_current()
# logging.info(info)

# # Retrieve a thumbnail for a specific piece of art. Returns a JPEG.
# thumbnail = tv.art().get_thumbnail('MY_F0026')

# # # Set a piece of art
# # tv.art().select_image('SAM-F0206')

# # # Set a piece of art, but don't immediately show it if not in art mode
# # tv.art().select_image('SAM-F0201', show=False)

# # Determine whether the TV is currently in art mode
# info = tv.art().get_artmode()
# logging.info(info)

# # Switch art mode on or off
# # tv.art().set_artmode(True)
# tv.art().set_artmode(False)

# # # Upload a picture
# # file = open('test.png', 'rb')
# # data = file.read()
# # tv.art().upload(data)

# # # If uploading a JPEG
# # tv.art().upload(data, file_type='JPEG')

# # # To set the matte to modern and apricot color
# # tv.art().upload(data, matte='modern_apricot')

# # # Delete an uploaded item
# # tv.art().delete('MY-F0020')

# # # Delete multiple uploaded items
# # tv.art().delete_list(['MY-F0020', 'MY-F0021'])

# # # List available photo filters
# # info = tv.art().get_photo_filter_list()
# # logging.info(info)

# # # Apply a filter to a specific piece of art
# # tv.art().set_photo_filter('SAM-F0206', 'ink')

# Generate an image through Dalle
