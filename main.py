import os
from time import sleep
import socket
from waveshare_epd import epd2in7
from PIL import Image, ImageDraw, ImageFont
from gpiozero import Button

epd = epd2in7.EPD() # get the display
epd.init()           # initialize the display
print("Clear...")    # prints to console, not the display, for debugging
epd.Clear(0xff)

def get_ip_address():
    ip_address = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

def printToDisplay(string):
    HBlackImage = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(HBlackImage)  # Create draw object and pass in the image layer we want to work with (HBlackImage)
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSerif.ttf',30)  # Create our font, passing in the font file and font size
    draw.text((25, 65), string, font=font, fill=0)
    epd.display(epd.getbuffer(HBlackImage))

while True:
    ip = ''
    try:
        ip = get_ip_address()
        if ip:
            printToDisplay(ip)
            print(ip)
            break
        else:
            printToDisplay('Getting IP')
            sleep(5)
    except:
        printToDisplay('Getting IP')
        sleep(5)
