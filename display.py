# Modules
import sys
import os
from var import libdir
from TP_lib import icnt86
from TP_lib import epd2in9_V2
import asyncio
import time
import logging

# Functions and variables

epd = epd2in9_V2.EPD_2IN9_V2()

tp = icnt86.INCT86()

ICNT_Dev = icnt86.ICNT_Development()
ICNT_Old = icnt86.ICNT_Development()

#logging.basicConfig(level=logging.DEBUG)
flag_t = 1

def init():
    try:
        logging.info("epd2in9_V2 Touch Demo")
        logging.info("init and Clear")
        epd.init()
        tp.ICNT_Init()
        epd.Clear(0xFF)
    except IOError as e:
        logging.info(e)

async def touchme():
    logging.debug("pthread irq running")
    while flag_t == 1:
        if(tp.digital_read(tp.INT) == 0) :
            ICNT_Dev.Touch = 1
            tp.ICNT_Scan(ICNT_Dev, ICNT_Old)
            x = ICNT_Dev.X[0]
            logging.debug(f"A touch was detected at x-coordinate {x}")
            from touch import press_detected
            await press_detected(x)
        else :
            ICNT_Dev.Touch = 0
        await asyncio.sleep(0.01)
    logging.debug("thread irq: exit")

async def display_screen(screen_img):
    epd.display_Base(epd.getbuffer(screen_img))
    logging.debug("Showing image")

async def shutdown():
    logging.info("ctrl + c:")
    flag_t = 0
    epd.sleep()
    time.sleep(2)
    t1.join()
    epd.Dev_exit()
    exit()