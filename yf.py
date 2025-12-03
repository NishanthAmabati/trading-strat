import yfinance as yf
import pandas as pd

class YfMethods:
    def __init__(self):
        pass

    def get_ohlc(self, ticker: str, period: str="36d", interval: str="1h"):
        self.ticker=ticker
        self.period=period
        self.interval=interval

        df = yf.Ticker(self.ticker).history(period=self.period, interval=self.interval)

        return df