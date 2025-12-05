import yfinance as yf
import pandas as pd
from sr_detector import Candle, SRDetector
from yf import YfMethods, DEFAULT_TIMEFRAMES
from typing import List, Tuple

# Configuration constants
MIN_CANDLES_FOR_ANALYSIS = 50


def dataframe_to_candles(dataframe: pd.DataFrame) -> List[Candle]:
    """Convert a pandas DataFrame to a list of Candle objects."""
    candles = []
    for _, row in dataframe.iterrows():
        candles.append(Candle(
            open=float(row.Open),
            high=float(row.High),
            low=float(row.Low),
            close=float(row.Close)
        ))
    return candles


def print_separator(char: str = "=", length: int = 60):
    """Print a separator line."""
    print(char * length)


def print_header(title: str, char: str = "=", length: int = 60):
    """Print a formatted header."""
    print()
    print_separator(char, length)
    print(f"  {title}")
    print_separator(char, length)


def print_sr_levels(
    ticker: str,
    interval: str,
    period: str,
    current_price: float,
    support: List[float],
    resistance: List[float]
):
    """Print support and resistance levels in a formatted way."""
    print(f"\n📊 {ticker} | Timeframe: {interval} | Period: {period}")
    print(f"   Current Price: {current_price:.2f}" if current_price else "   Current Price: N/A")
    
    print(f"\n   🟢 SUPPORT LEVELS (below current price):")
    if support:
        for i, s in enumerate(support, 1):
            distance = current_price - s if current_price else 0
            pct = (distance / current_price * 100) if current_price else 0
            print(f"      S{i}: {s:.2f} (↓ {distance:.2f} pts | {pct:.2f}%)")
    else:
        print("      No support levels detected")
    
    print(f"\n   🔴 RESISTANCE LEVELS (above current price):")
    if resistance:
        for i, r in enumerate(resistance, 1):
            distance = r - current_price if current_price else 0
            pct = (distance / current_price * 100) if current_price else 0
            print(f"      R{i}: {r:.2f} (↑ {distance:.2f} pts | {pct:.2f}%)")
    else:
        print("      No resistance levels detected")
    
    print("-" * 50)


def analyze_ticker(
    yfmethods: YfMethods,
    ticker: str,
    timeframes: List[Tuple[str, str]] = None
):
    """
    Analyze a single ticker across multiple timeframes.
    
    Args:
        yfmethods: YfMethods instance
        ticker: Ticker symbol
        timeframes: List of (interval, period) tuples
    """
    if timeframes is None:
        timeframes = DEFAULT_TIMEFRAMES
    
    # Get current price once
    try:
        current_price = yfmethods.get_currentprice(ticker)
    except Exception as e:
        print(f"⚠️  Warning: Could not fetch current price for {ticker}: {e}")
        current_price = None
    
    print_header(f"ANALYSIS: {ticker}")
    
    for interval, period in timeframes:
        try:
            df = yfmethods.get_ohlc(ticker, period=period, interval=interval)
            
            if df.empty:
                print(f"\n⚠️  No data available for {ticker} {interval}/{period}")
                continue
            
            candles = dataframe_to_candles(df)
            
            # Adjust detector parameters based on timeframe
            detector = SRDetector()
            
            # Need at least minimum candles to analyze
            if len(candles) < MIN_CANDLES_FOR_ANALYSIS:
                print(f"\n⚠️  Insufficient data for {ticker} {interval}: only {len(candles)} candles")
                continue
            
            support, resistance = detector.get_sr(candles)
            
            # Use last candle close if current price not available
            display_price = current_price if current_price else candles[-1].close
            
            print_sr_levels(ticker, interval, period, display_price, support, resistance)
            
        except Exception as e:
            print(f"\n❌ Error analyzing {ticker} {interval}/{period}: {e}")


def main():
    """Main function to run the analysis."""
    # Define tickers to analyze
    tickers = ["^NSEI", "^NSEBANK"]
    
    # Define timeframes: (interval, period)
    timeframes = [
        ("1h", "36d"),
        ("30m", "20d"),
        ("15m", "10d"),
        ("5m", "1d"),
    ]
    
    print_header("SUPPORT & RESISTANCE ANALYZER", "═", 60)
    print(f"Analyzing {len(tickers)} ticker(s) across {len(timeframes)} timeframe(s)")
    
    yfmethods = YfMethods()
    
    for ticker in tickers:
        analyze_ticker(yfmethods, ticker, timeframes)
    
    # Print summary
    print_header("ANALYSIS COMPLETE", "═", 60)
    print(f"✅ Analyzed: {', '.join(tickers)}")
    print(f"📈 Timeframes: {', '.join([f'{i}/{p}' for i, p in timeframes])}")


if __name__ == "__main__":
    main()