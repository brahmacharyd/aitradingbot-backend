import json
import yfinance as yf
import pandas as pd
import time
import random
from strategy_manager import apply_strategies

symbols = ["BTC-USD", "ETH-USD", "SOL-USD", "BNB-USD", "XRP-USD"]

def fetch_data(symbol):
    data = yf.download(symbol, interval="15m", period="1d", progress=False)
    if isinstance(data.columns[0], tuple):
        data.columns = [col[0].lower() for col in data.columns]
    else:
        data.columns = [col.lower() for col in data.columns]
    return data.dropna()

def generate_signals():
    all_signals = []
    for symbol in symbols:
        try:
            data = fetch_data(symbol)
            symbol_signals = apply_strategies(symbol, data)
            all_signals.extend(symbol_signals)
        except Exception as e:
            print(f"❌ Error for {symbol}: {e}")
    return all_signals

def main():
    signals = generate_signals()
    print(json.dumps(signals, indent=2))  # 🟢 Keep for debugging
    return signals  # ✅ Return signals to the caller

if __name__ == "__main__":
    main()
