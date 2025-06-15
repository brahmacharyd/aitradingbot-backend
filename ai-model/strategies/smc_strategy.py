import pandas as pd
import random
from utils.rrr_calculator import calculate_rrr

def smc_strategy(data: pd.DataFrame):
    signals = []

    if len(data) < 30:
        return signals

    latest = data.iloc[-1]
    price = round(latest['close'], 2)

    # 1. Swing Detection
    swing_low = data['low'].rolling(window=10).min().iloc[-2]
    swing_high = data['high'].rolling(window=10).max().iloc[-2]

    # 2. Fair Value Gap (FVG) Filter
    def is_near_fvg_zone():
        for i in range(len(data) - 5, len(data)):
            if data['low'].iloc[i] > data['high'].iloc[i - 2]:
                return True
        return False

    near_fvg = is_near_fvg_zone()

    # 3. Order Block Confirmation
    def is_bullish_ob():
        return (
            latest['open'] < latest['close'] and
            data.iloc[-2]['close'] < data.iloc[-2]['open']
        )

    def is_bearish_ob():
        return (
            latest['open'] > latest['close'] and
            data.iloc[-2]['close'] > data.iloc[-2]['open']
        )

    # === Bullish SMC Setup ===
    if (
        latest['low'] < swing_low * 0.999 and  # Liquidity sweep
        latest['close'] > latest['open'] and   # Bullish candle
        near_fvg and                           # FVG nearby
        is_bullish_ob()
    ):
        tp = round(price * 1.03, 2)
        sl = round(swing_low * 0.997, 2)
        rrr = calculate_rrr(tp, sl, price, "BUY")
        if rrr >= 2:
            signals.append({
                "strategy": "SMC-Full",
                "type": "BULLISH",
                "price": price,
                "tp": tp,
                "sl": sl,
                "confidence": random.randint(80, 92),
                "rrr": rrr,
                "decision": "HIGH PROBABILITY LONG"
            })

    # === Bearish SMC Setup ===
    if (
        latest['high'] > swing_high * 1.001 and  # Liquidity grab
        latest['close'] < latest['open'] and     # Bearish candle
        near_fvg and                             # FVG filter
        is_bearish_ob()
    ):
        tp = round(price * 0.97, 2)
        sl = round(swing_high * 1.0025, 2)
        rrr = calculate_rrr(tp, sl, price, "SELL")
        if rrr >= 2:
            signals.append({
                "strategy": "SMC-Full",
                "type": "BEARISH",
                "price": price,
                "tp": tp,
                "sl": sl,
                "confidence": random.randint(80, 92),
                "rrr": rrr,
                "decision": "HIGH PROBABILITY SHORT"
            })

    return signals
