from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in7
from datetime import datetime
import textwrap
import socket
from usgs_api import *

import krakenex

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
    return (epd2in7.EPD_WIDTH - width), height

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
    draw = ImageDraw.Draw(HBlackImage)  # Create draw object and pass in the image layer we want to work with (HBlackImage)
    font_size=20
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSerif.ttf', font_size)
    time_text = datetime.now().strftime(date_format)
    x_offset, height = center_text_offset(time_text, font, font_size)
    draw.text((x_offset * 2 ,y_offset), time_text, font=font, fill=0)
    y_offset += height + 5
    draw.line((0, y_offset, HBlackImage.size[0], y_offset), fill=0, width=3)

    epd.display(epd.getbuffer(HBlackImage))

def print_usgs(epd):
    y_offset = 0
    HBlackImage = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(
        HBlackImage)  # Create draw object and pass in the image layer we want to work with (HBlackImage)
    font_size = 20
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSerif.ttf', font_size)
    time_text = datetime.now().strftime(date_format)
    x_offset, height = center_text_offset(time_text, font, font_size)
    draw.text((x_offset * 2, y_offset), time_text, font=font, fill=0)
    y_offset += height + 5
    draw.line((0, y_offset, HBlackImage.size[0], y_offset), fill=0, width=3)

    for site in southwest:
        ld = get_most_recent_value(get_site_data(site).json())
        ld_min = ((datetime.now(local_tz) - ld).seconds / 60)
        draw.text((3, y_offset), site['name'], font=font, fill=0)


    epd.display(epd.getbuffer(HBlackImage))

def print_crypto(coins):
    y_offset = 0
    HBlackImage = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
    draw = ImageDraw.Draw(
        HBlackImage)  # Create draw object and pass in the image layer we want to work with (HBlackImage)
    font_size = 20
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSerif.ttf', font_size)
    time_text = datetime.now().strftime(date_format)
    x_offset, height = center_text_offset(time_text, font, font_size)
    draw.text((x_offset * 2, y_offset), time_text, font=font, fill=0)
    y_offset += height + 5
    draw.line((0, y_offset, HBlackImage.size[0], y_offset), fill=0, width=3)

    for coin in coins:
        coin_text = f"{str(coin)} - ${round(coins[coin]['price'], 4)}"
        print(coin_text)
        draw.text((5, y_offset), coin_text, font=font, fill=0)
        y_offset += 20
        draw.line((0, y_offset, HBlackImage.size[0], y_offset), fill=0, width=3)

    epd.display(epd.getbuffer(HBlackImage))

def kraken_price(coin):
    client = krakenex.API()
    pair = f'{coin}USD'
    r = client.query_public('Depth', {'pair': pair, 'count': '1'})
    asks = float(r['result'][pair]['asks'][0][0]) * float(r['result'][pair]['asks'][0][1])
    bids = float(r['result'][pair]['bids'][0][0]) * float(r['result'][pair]['bids'][0][1])
    vol = float(r['result'][pair]['asks'][0][1]) + float(r['result'][pair]['bids'][0][1])
    client.close()
    return (asks + bids)/vol

def get_coin_prices():
    coins = {'XBT':{'symbol':'XXBTZ'}, 'XLM': {'symbol':'XXLMZ'}, 'XDG':{'symbol':'XDG'}}
    for coin in coins:
        coins[coin]['price'] = kraken_price(coins[coin]['symbol'])
    return coins