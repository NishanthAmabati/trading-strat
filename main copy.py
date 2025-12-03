from dotenv import load_dotenv
from kiteconnect import KiteConnect
import os
import logging
import datetime as dt
import pandas as pd

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

api_key=os.getenv("api_key")
access_token=os.getenv("access_token")

kite=KiteConnect(api_key=api_key)
#kite.set_access_token(access_token)

kite.set_access_token("oCjDDUTLqCnIRRQ12ac4uaiJ2A1OYa3R")

kite.profile()

#instrument_token = ""
#interval = os.getenv("")

#to_date = os.getenv("")
#from_date = to_date - dt.timedelta(days=3)

#data = kite.historical_data(
#    instrument_token,
#    from_date,
#    to_date,
#    interval
#)

#df = pd.DataFrame(data)
#print (df)