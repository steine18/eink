import os
from helpers import *
from datetime import datetime, timedelta
from time import sleep
from waveshare_epd import epd2in7
from PIL import Image, ImageDraw, ImageFont
from gpiozero import Button
from usgs_api import *

date_format = '%Y-%m-%d %H:%M'

epd = epd2in7.EPD()  # get the display
epd.init()           # initialize the display
print("Clear...")    # prints to console, not the display, for debugging
epd.Clear(0xff)


# Define Buttons
btn0 = Button(5)
btn1 = Button(6)
btn2 = Button(13)
btn3 = Button(19)




def bp0():
    global NEXT_SCREEN
    NEXT_SCREEN = 0


def bp1():
    global NEXT_SCREEN
    NEXT_SCREEN = 1


def bp2():
    global NEXT_SCREEN
    NEXT_SCREEN = 2


def bp3():
    global NEXT_SCREEN
    NEXT_SCREEN = 3


btn0.when_pressed = bp0
btn1.when_pressed = bp1
btn2.when_pressed = bp2
btn3.when_pressed = bp3

# Globals
CURRENT_SCREEN = 0
NEXT_SCREEN = None
REFRESH_INTERVAL = 1  # Minutes
REFRESH_TIME = datetime.now()

while True:
    if NEXT_SCREEN is not None:
        CURRENT_SCREEN = NEXT_SCREEN
        REFRESH_TIME = datetime.now()
        NEXT_SCREEN = None
        print(CURRENT_SCREEN)
    if CURRENT_SCREEN == 0 and REFRESH_TIME < datetime.now():
        ip = ''
        try:
            ip = get_ip_address()
            if ip:
                printToDisplay(ip, epd)
                print(ip)
                # break
                REFRESH_TIME = datetime.now() + timedelta(minutes=60)
        except:
            printToDisplay('Getting IP', epd)
            sleep(5)
    elif CURRENT_SCREEN == 1 and REFRESH_TIME < datetime.now():
        sites = update_sites(southwest)
        print_usgs(sites, epd)
        REFRESH_TIME = datetime.strptime(datetime.now().strftime(date_format), date_format) + timedelta(minutes=1)
    elif CURRENT_SCREEN == 2 and REFRESH_TIME < datetime.now():
        coins = get_coin_prices()
        print_crypto(coins, epd)
        REFRESH_TIME = datetime.strptime(datetime.now().strftime(date_format), date_format) + timedelta(minutes=1)
    elif CURRENT_SCREEN == 3 and REFRESH_TIME is not None:
        epd.Clear(0xff)
        REFRESH_TIME = None
