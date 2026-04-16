# Modules
#import sys
#import os
from var import libdir
from TP_lib import epd2in9_V2
import asyncio
import math
#import time
import logging


# Functions and variables
from screens import make_idlescreen, make_paymentsscreen, make_salesscreen
from var import current_screen

height = epd2in9_V2.EPD_HEIGHT
quadrant_size = height/4

# Mappings

# 0 = idlescreen
# 1 = salesscreen
# 2 = successscreen
# 3 = paymentsscreen
# 4 = failurescreen

mapping = [make_idlescreen, make_salesscreen, "make_successscreen", make_paymentsscreen, "make_failurescreen"]

menu = [
        [1, 1, 1, 1], # 0 Idle Screen
        [3, 0, 0, 0], # 1 Sales Screen
        [3, 0, 0, 0], # 2 Success Screen
        [0, 0, 0, 0], # 3 Payments Screen
        [0, 0, 0, 0]  # Failure Screen
        ]

# Screens

async def press_detected(x):
    global current_screen
    quadrant = int(math.floor(x / quadrant_size))
    logging.debug(f"Quadrant determined: {quadrant}")
    logging.debug(f"Current screen: {current_screen}")
    await set_screen(menu[current_screen][quadrant])
    await mapping[current_screen]()

async def set_screen(set_current_screen):
    global current_screen
    current_screen = set_current_screen
    logging.debug(f"Next screen: {current_screen}")