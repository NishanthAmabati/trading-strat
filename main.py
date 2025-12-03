import yfinance as yf
import pandas as pd
from sr_detector import Candle, SRDetector
from yf import YfMethods


def dataframe_to_candles(dataframe):
    candles = []
    for _, row in df.iterrows():
        candles.append(Candle(
            open=float(row.Open),
            high=float(row.High),
            low=float(row.Low),
            close=float(row.Close)
        ))
    return candles

if __name__ == "__main__":
    print("Fetching nifty data...")
    yfmethods=YfMethods()
    df = yfmethods.get_ohlc("^NSEI")

    candles = dataframe_to_candles(df)
    print(f"Total 1H candles: {len(candles)}")

    detector = SRDetector()
    support, resistance = detector.get_sr(candles)

    print("\n===== SUPPORT LEVELS =====")
    for s in support:
        print(round(s, 2))

    print("\n===== RESISTANCE LEVELS =====")
    for r in resistance:
        print(round(r, 2))