#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic/2in9')
fontdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')

#picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic/2in9')
#fontdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
#libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
    
from TP_lib import icnt86
from TP_lib import epd2in9_V2
from TP_lib import weather_2in9_V2

import asyncio
import time
import logging
from PIL import Image, ImageDraw, ImageFont
import traceback
import threading

logging.basicConfig(level=logging.DEBUG)
flag_t = 1

epd = epd2in9_V2.EPD_2IN9_V2()

tp = icnt86.INCT86()

ICNT_Dev = icnt86.ICNT_Development()
ICNT_Old = icnt86.ICNT_Development()

def init():
    try:
        logging.info("epd2in9_V2 Touch Demo")
        logging.info("init and Clear")
        epd.init()
        tp.ICNT_Init()
        epd.Clear(0xFF)

    except IOError as e:
        logging.info(e)

async def pthread_irq():
    print("pthread irq running")
    while flag_t == 1:
        if(tp.digital_read(tp.INT) == 0) :
            ICNT_Dev.Touch = 1
            tp.ICNT_Scan(ICNT_Dev, ICNT_Old)
        else :
            ICNT_Dev.Touch = 0
        await asyncio.sleep(0.01)
    print("thread irq: exit")