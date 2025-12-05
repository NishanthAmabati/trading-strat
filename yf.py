import yfinance as yf
import pandas as pd
from typing import List, Dict, Tuple, Optional

# Default timeframes: (interval, period)
DEFAULT_TIMEFRAMES = [
    ("1h", "36d"),
    ("30m", "20d"),
    ("15m", "10d"),
    ("5m", "1d"),
]

class YfMethods:
    def __init__(self):
        pass

    def get_currentprice(self, ticker: str) -> float:
        """Get the current price for a single ticker."""
        return yf.Ticker(ticker).fast_info['last_price']

    def get_ohlc(self, ticker: str, period: str = "20d", interval: str = "30m") -> pd.DataFrame:
        """Get OHLC data for a single ticker with specified period and interval."""
        df = yf.Ticker(ticker).history(period=period, interval=interval)
        return df

    def get_ohlc_multi(
        self, 
        tickers: List[str], 
        timeframes: List[Tuple[str, str]] = None
    ) -> Dict[str, Dict[str, pd.DataFrame]]:
        """
        Get OHLC data for multiple tickers across multiple timeframes.
        
        Args:
            tickers: List of ticker symbols (e.g., ["^NSEI", "^NSEBANK"])
            timeframes: List of (interval, period) tuples. 
                        Defaults to [(1h, 36d), (30m, 20d), (15m, 10d), (5m, 1d)]
        
        Returns:
            Nested dict: {ticker: {interval: DataFrame}}
            Example: {"^NSEI": {"1h": df1, "30m": df2, ...}}
        """
        if timeframes is None:
            timeframes = DEFAULT_TIMEFRAMES
        
        result = {}
        for ticker in tickers:
            result[ticker] = {}
            for interval, period in timeframes:
                try:
                    df = yf.Ticker(ticker).history(period=period, interval=interval)
                    result[ticker][interval] = df
                except (KeyError, ValueError, ConnectionError, TimeoutError) as e:
                    print(f"Warning: Failed to fetch {ticker} {interval}/{period}: {e}")
                    result[ticker][interval] = pd.DataFrame()
        
        return result

    def get_current_prices(self, tickers: List[str]) -> Dict[str, Optional[float]]:
        """Get current prices for multiple tickers."""
        prices = {}
        for ticker in tickers:
            try:
                prices[ticker] = yf.Ticker(ticker).fast_info['last_price']
            except (KeyError, ValueError, ConnectionError, TimeoutError) as e:
                print(f"Warning: Failed to get price for {ticker}: {e}")
                prices[ticker] = None
        return prices