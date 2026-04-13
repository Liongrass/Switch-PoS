# Modules
import logging
import requests

# Functions and variables
from var import acl_api_token, currency, lnbits_server, lnbits_wallet, lnurl, price, switch_title, ws_switch, x_api_key

url_base_switch = "https://" + lnbits_server + "/bitcoinswitch/api/v1"
url_base_payments = "https://" + lnbits_server + "/api/v1/payments"


def get_headers():
	global headers
	if web_setup == True:
		headers = {"X-Api-Key" : x_api_key, "Content-type" : "application/json"}
	else:
		headers = {'accept' : 'application/json', 'Authorization' : f'Bearer {acl_api_token}'}
	return headers

def get_payments():
	payments_request = requests.get(url_base_payments, headers=get_headers())
	payments = payments_request.json()
	amount = payments[0]['amount']/1000
	logging.info(f"Payment received: {amount} satoshi")
	return amount

#https://send.laisee.org/bitcoinswitch/api/v1/lnurl/{bitcoinswitch_id}
#https://send.laisee.org/bitcoinswitch/api/v1/public/{bitcoinswitch_id}

'''
1. Get list of Bitcoin Switches
2. Check if switch already exists (identified by name)
3. Register switch
4. Update switch
5. Retrieve LNURL
6. Listen to websockets
'''