# Modules
import logging
import requests

# Functions and variables
from var import acl_api_token, currency, lnbits_server, lnbits_wallet, lnurl, price, switch_title, ws_switch, x_api_key

url_base_switch = "https://" + lnbits_server + "/bitcoinswitch/api/v1"
url_base_payments = "https://" + lnbits_server + "/api/v1/payments"


def get_headers():
	global headers
	headers = {"X-Api-Key" : x_api_key, "Content-type" : "application/json"}
	return headers

def get_payments():
	payments_request = requests.get(url_base_payments, headers=get_headers())
	payments = payments_request.json()
	#print(payments)
	#amount = payments[0]['amount']/1000
	#logging.info(f"Payment received: {amount} satoshi")
	return payments