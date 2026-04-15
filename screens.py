# Modules
from datetime import datetime
import logging
import os
from PIL import Image, ImageDraw, ImageFont
import qrcode
from time import sleep
import time
from TP_lib import epd2in9_V2

# Functions and variables
from display import display_screen
from lnbits import get_payments
from var import lnurl, fontA, fontB, fontBs, picdir, suggested_wallets

canvas_width = epd2in9_V2.EPD_WIDTH
canvas_height = epd2in9_V2.EPD_HEIGHT

def canvas():
    canvas = Image.new('1', (canvas_width, canvas_height), 'white')
    draw = ImageDraw.Draw(canvas)
    box = [0, 222, 128, 296]
    draw.rectangle(xy=box, fill="black", width=5)
    return canvas

def coordinates(img):
    x_center = (canvas_width - img.width) // 2
    y_center = (canvas_height - img.height) // 2
    qr_offset = 0
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
		if suggested_wallets.index(i) % 2 == 0:
			o = 0
		else:
			o = 1
		load_pics(i, 40)
		#img.paste(pic_img_s, (44, 85 + suggested_wallets.index(i) * 60))
		img.paste(pic_img_s, (16 + o * 56, 85 + int(round(((suggested_wallets.index(i)- 0.5)/2), 0)) * 60))
		#draw.text((64, 75 + suggested_wallets.index(i) * 60), i, font = fontA, anchor="mm")
	draw.text((64, 250), "Press anywhere", font = fontBs, fill="white", anchor="mm")
	draw.text((64, 275), "to continue", font = fontBs, fill="white", anchor="mm")
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
	draw.text((64, 250), "Press for", font = fontBs, fill="white", anchor="mm")
	draw.text((64, 275), "transactions", font = fontBs, fill="white", anchor="mm")
	await display_screen(img)

async def make_sucessscreen(incoming_payments, comment):
	img = canvas()
	draw = ImageDraw.Draw(img)
	draw.text((canvas_width/2, 5), "Payment", font = fontB, anchor="ma")
	draw.text((canvas_width/2, 40), "Received", font = fontB, anchor="ma")
	draw.text((canvas_width/2, 80), str(round(incoming_payments[0]['extra']['wallet_fiat_amount'],2)), font = fontB, anchor="ma")
	draw.text((canvas_width/2, 110), incoming_payments[0]['extra']['wallet_fiat_currency'], font = fontBs, anchor="ma")
	draw.text((canvas_width/2, 130), str(incoming_payments[0]['amount']/1000) + " sat", font = fontA, anchor="ma")
	draw.text((64, 250), "Press for", font = fontBs, fill="white", anchor="mm")
	draw.text((64, 275), "transactions", font = fontBs, fill="white", anchor="mm")
	await display_screen(img)

async def make_paymentsscreen():
	incoming_payments = get_payments()
	img = canvas()
	draw = ImageDraw.Draw(img)
	'''
	datetime_string = "2026-04-13T21:45:35.712978+00:00"
	datetime_object = datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S.%f%z")
	#timestamp = datetime_object.timestamp()
	formatted_string = datetime_object.strftime("%H:%M")
	print("Time:", formatted_string)
	'''

	draw.text((canvas_width/2, 5), "RECEIVED", font = fontB, anchor="ma")
	#current_date = time.strftime("%Y %B %d")
	current_date = datetime.now().astimezone().strftime("%Y %B %d")
	draw.text((canvas_width/2, 40), current_date, font = fontA, anchor="mm")

	for i in incoming_payments[:3]:
		#print("TIME")
		#print(i['time'])
		#print(datetime.strptime(i['time'], "%Y-%m-%dT%H:%M:%S.%f%z").astimezone().strftime("%H:%M"))
		draw.text((canvas_width/2, 65 + incoming_payments.index(i)*50), str(datetime.strptime(i['time'], "%Y-%m-%dT%H:%M:%S.%f%z").astimezone().strftime("%H:%M")), font = fontA, anchor="mm")	
		draw.text((canvas_width/2 -2, 85 + incoming_payments.index(i)*50), str(round(i['extra']['wallet_fiat_amount'],2)), font = fontBs, anchor="rm")
		draw.text((canvas_width/2 +2, 85 + incoming_payments.index(i)*50), i['extra']['wallet_fiat_currency'], font = fontBs, anchor="lm")
		draw.text((canvas_width/2, 97 + incoming_payments.index(i)*50), str(i['amount']/1000) + " sat", font = fontA, anchor="mm")

	draw.text((64, 250), "Press anywhere", font = fontBs, fill="white", anchor="mm")
	draw.text((64, 275), "to return", font = fontBs, fill="white", anchor="mm")
	await display_screen(img)
