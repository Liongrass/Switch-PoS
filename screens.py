# Modules
import logging
import os
from PIL import Image, ImageDraw, ImageFont
import qrcode
from time import sleep
from TP_lib import epd2in9_V2

# Functions and variables
from display import display_screen
from var import lnurl, fontA, fontB, fontBs, picdir, suggested_wallets

canvas_width = epd2in9_V2.EPD_WIDTH
canvas_height = epd2in9_V2.EPD_HEIGHT

def canvas():
    canvas = Image.new('1', (canvas_width, canvas_height), 'white')
    return canvas

def coordinates(img):
    x_center = (canvas_width - img.width) // 2
    y_center = (canvas_height - img.height) // 2
    qr_offset = 70
    global paste_box
    paste_box = (x_center, y_center + qr_offset, x_center + img.width, y_center + img.height + qr_offset)
    return paste_box

def load_pics(i, pic_size):
    pic_img = Image.open(os.path.join(picdir, i + '_100x100.bmp'))
    global pic_img_s
    pic_img_s = pic_img.resize((pic_size, pic_size))
    return pic_img_s

def make_qrcode():
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=3,
        border=1,
        )
    qr.add_data(lnurl)
    qr.make(fit=True)
    global qr_img
    qr_img = qr.make_image(fill_color='black', back_color='white')
    qr_img = qr_img.convert("1")
    qr_coordinates = coordinates(qr_img)
    logging.debug(f"QR coordinates: {qr_coordinates}")
    global qr_width
    qr_width = qr_img.width
    logging.debug(f"QR Code Width: {qr_width}")
    return qr_img

async def make_idlescreen():
	img = canvas()
	draw = ImageDraw.Draw(img)
	draw.text((canvas_width/2, 5), "Pay with\nLightning", font = fontB, anchor="ma")
	for i in suggested_wallets:
		load_pics(i, 40)
		img.paste(pic_img_s, (44, 85 + suggested_wallets.index(i) * 60))
		draw.text((64, 75 + suggested_wallets.index(i) * 60), i, font = fontA, anchor="mm")
	draw.text((64, 260), "Press anywhere", font = fontBs, anchor="mm")
	draw.text((64, 280), "to continue", font = fontBs, anchor="mm")
	await display_screen(img)

'''
def make_idlescreen(error):
    initialize()
    global idle_img
    #idle_img = Image.open(os.path.join(picdir, '21UP_h.bmp'))
    idle_img = canvas()
    display_screen(idle_img)
    draw = ImageDraw.Draw(idle_img)
    draw.text((140, 20), "Pay with Lightning", font = fontB, anchor="ma")
    display_overlay(idle_img)

    for i in suggested_wallets:
        load_pics(i, 40)
        idle_img.paste(pic_img_s, (35, 70 + suggested_wallets.index(i) * 50))
        draw.text((85, 90 + suggested_wallets.index(i) * 50), i, font = fontA, anchor="lm")
        display_overlay(idle_img)
    if error == False:
        draw.text((140, 215 + 6*40), f"ANY POP", font = fontA, anchor="ma")
        display_overlay(idle_img)
        draw.text((140, 175 + 5*40), f"{price} {currency}", font = fontBL, anchor="ma")
        display_overlay(idle_img)
        make_qrcode()
        idle_img.paste(qr_img, paste_box)
        display_overlay(idle_img)
    else:
        draw.text((140, 205 + 6*40), "CONNECTION ERROR", font = fontB, anchor="ma")

    logging.debug(idle_img)
    display_overlay(idle_img)
'''

async def make_salesscreen():
	img = canvas()
	make_qrcode()
	img.paste(qr_img, paste_box)
	draw = ImageDraw.Draw(img)
	draw.text((canvas_width/2, 20), "PAY NOW", font = fontB, anchor="ma")
	await display_screen(img)

async def make_sucessscreen(payments, comment):
	img = canvas()
	draw = ImageDraw.Draw(img)
	draw.text((canvas_width/2, 5), "Payment", font = fontB, anchor="ma")
	draw.text((canvas_width/2, 40), "Received", font = fontB, anchor="ma")
	print("WATCH THIS")
	print(payments[0]['extra']['wallet_fiat_amount'])
	print(payments[0]['extra']['wallet_fiat_currency'])
	draw.text((canvas_width/2, 80), str(round(payments[0]['extra']['wallet_fiat_amount'],2)), font = fontB, anchor="ma")
	draw.text((canvas_width/2, 110), payments[0]['extra']['wallet_fiat_currency'], font = fontBs, anchor="ma")
	draw.text((canvas_width/2, 130), str(payments[0]['amount']/1000) + " sat", font = fontA, anchor="ma")


	await display_screen(img)