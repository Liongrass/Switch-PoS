# Modules
import asyncio
import logging
import websockets

# Functions and variables
from display import shutdown
from lnbits import get_payments
from screens import make_sucessscreen #make_confirmation_screen, make_idlescreen, make_success_overlay
#from trigger import pulse
from touch import mapping
from var import ws_switch

####### VARIABLES ########

async def listener():
    global current_screen
    while True:
        try:
            async with websockets.connect(ws_switch) as websocket:
                logging.info(f"Connected to {ws_switch}. Listening for incoming payments.")
                response_str = await websocket.recv()
                logging.debug(f"Message received: {response_str}")
                response = response_str.split("-")
                pin = response[0]
                duration = int(response[1])
                # Check for a comment
                global comment
                try:
                    response[2]
                except IndexError:
                    comment = ""
                    logging.debug("No comment submitted.")
                else:
                    comment = response[2]
                logging.debug(f"Incoming message: {response}")
                payments = get_payments()
                logging.info(f"Received payment over {payments[0]['extra']['wallet_fiat_amount']} {payments[0]['extra']['wallet_fiat_currency']} ({payments[0]['amount']/1000} satoshi)")
                current_screen = 2
                logging.debug(f"Current screen: {mapping[current_screen]}")
                await make_sucessscreen(payments, comment)
                #pulse(pin, duration)
                #logging.debug(f"Waiting {suceess_screen_expiry}s")
                #await asyncio.sleep(suceess_screen_expiry)
                #make_confirmation_screen(amount, comment)
                #logging.debug(f"Waiting {suceess_screen_expiry}s")
                #await asyncio.sleep(suceess_screen_expiry)
        except websockets.exceptions.WebSocketException as e: 
            logging.error(f"ERROR: {e}")
            error = e
            #make_idlescreen(error)
            sleep(suceess_screen_expiry)
        except asyncio.CancelledError:
            await shutdown()