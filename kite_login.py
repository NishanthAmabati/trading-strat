import logging
import os
from dotenv import load_dotenv
from kiteconnect import KiteConnect

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

api_key=os.getenv("api_key")
api_secret=os.getenv("secret_key")
request_token=os.getenv("request_token")
access_token=os.getenv("access_token")

kite = KiteConnect(api_key=api_key)
logging.info(kite.login_url())

try:
    kite.set_access_token(access_token)
    logging.info(f'set access token success')
except Exception as e:
    logging.error(f'set access token error {e}')

# Redirect the user to the login url obtained
# from kite.login_url(), and receive the request_token
# from the registered redirect url after the login flow.
# Once you have the request_token, obtain the access_token
# as follows.

'''
try:
    data = kite.generate_session(request_token, api_secret=api_secret)
    kite.set_access_token(data["access_token"])
    logging.info(f'session generated" {data}')
    logging.info(f'access token: {data["access_token"]}')
except Exception as e:
    logging.error("error generating seesion:", e)
'''

# Fetch full profile
kite.profile()

# Fetch all orders
#kite.orders()

# Get instruments
#kite.instruments()

# Get mutual fund instruments
#kite.mf_instruments()