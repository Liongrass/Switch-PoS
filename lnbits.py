# Modules
from datetime import datetime, timedelta
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
	#print(payments[0]['time'])
	incoming_payments = [i for i in payments if i['amount'] > 0 and datetime.now().astimezone() - datetime.strptime(i['time'], "%Y-%m-%dT%H:%M:%S.%f%z").astimezone() < timedelta(hours=24)]
	for i in incoming_payments:
		print(i['time'])
	#print(datetime.strptime(incoming_payments[0]['time'], "%Y-%m-%dT%H:%M:%S.%f%z").astimezone())
	#print(datetime.now().astimezone())
	#print(datetime.now().astimezone() - datetime.strptime(incoming_payments[0]['time'], "%Y-%m-%dT%H:%M:%S.%f%z").astimezone())
	#print(timedelta(hours=24))
	#delta = [i for i in payments if datetime.now().astimezone() - datetime.strptime(i['time'], "%Y-%m-%dT%H:%M:%S.%f%z").astimezone() < timedelta(hours=24)]
	#for i in payments:
	#	delta = datetime.now().astimezone() - datetime.strptime(i['time'], "%Y-%m-%dT%H:%M:%S.%f%z").astimezone()# < timedelta(hours=24)
	#	print(delta)
	return incoming_payments