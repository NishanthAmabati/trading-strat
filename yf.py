import yfinance as yf
import pandas as pd

class YfMethods:
    def __init__(self):
        pass

    def get_currentprice(self, ticker: str):
        self.ticker=ticker
        return yf.Ticker(self.ticker).fast_info['last_price']

    def get_ohlc(self, ticker: str, period: str="20d", interval: str="30m"):
        self.ticker=ticker
        self.period=period
        self.interval=interval

        df = yf.Ticker(self.ticker).history(period=self.period, interval=self.interval)

        return df