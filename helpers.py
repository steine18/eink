from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in7
from datetime import datetime
import textwrap
import socket

date_format = '%Y-%m-%d %H:%M'

def get_ip_address():
    ip_address = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

def get_text_dimensions(text, font, font_size):
    ascent, descent = font.getmetrics()
    (width, baseline), (offset_x, offset_y) = font.font.getsize(text)
    return (width, baseline), (offset_x, offset_y)

def center_text_offset(text, font, font_size):
    (width, height), (offset_x, offset_y) = get_text_dimensions(text, font, font_size)
    return (epd2in7.EPD_WIDTH - width)/2, height

def printToDisplay(string, epd, font_size =10):
    x_offset = 0
    HBlackImage = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(HBlackImage)  # Create draw object and pass in the image layer we want to work with (HBlackImage)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSerif.ttf', font_size)  # Create our font, passing in the font file and font size
    draw.text((0, x_offset), string, font=font, fill=0)
    epd.display(epd.getbuffer(HBlackImage))

def print_main(epd):
    y_offset = 0
    HBlackImage = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(
    HBlackImage)  # Create draw object and pass in the image layer we want to work with (HBlackImage)
    font_size=20
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSerif.ttf', font_size)
    time_text = datetime.now().strftime(date_format)
    x_offset, height = center_text_offset(text, font, font_size)
    get_text_dimensions(time_text, font, font_size)
    draw.text((x_offset,y_offset), time_text, font=font, fill=0)
    y_offset += height
    epd.display(epd.getbuffer(HBlackImage))


