import random
from utils.rrr_calculator import calculate_rrr

def find_swing_highs_lows(data, lookback=3):
    swing_highs = []
    swing_lows = []

    for i in range(lookback, len(data) - lookback):
        high = data['high'].iloc[i]
        low = data['low'].iloc[i]

        # Swing High: surrounded by lower highs
        if all(high > data['high'].iloc[i - j] for j in range(1, lookback + 1)) and \
           all(high > data['high'].iloc[i + j] for j in range(1, lookback + 1)):
            swing_highs.append((i, high))

        # Swing Low: surrounded by higher lows
        if all(low < data['low'].iloc[i - j] for j in range(1, lookback + 1)) and \
           all(low < data['low'].iloc[i + j] for j in range(1, lookback + 1)):
            swing_lows.append((i, low))

    return swing_highs, swing_lows


def swing_strategy(data, lookback=3):
    results = []
    price = round(data['close'].iloc[-1], 2)

    swing_highs, swing_lows = find_swing_highs_lows(data, lookback)

    if not swing_highs or not swing_lows:
        return results

    last_swing_high = swing_highs[-1][1]
    last_swing_low = swing_lows[-1][1]

    # 🟢 Bullish Entry near Swing Low
    if price <= last_swing_low * 1.01:
        sl = round(last_swing_low * 0.997, 2)
        tp = round(price * 1.03, 2)
        rrr = calculate_rrr(tp, sl, price, "BUY")
        if rrr >= 1.2:
            results.append({
                "strategy": "WickSwingSupport",
                "type": "BULLISH",
                "price": price,
                "tp": tp,
                "sl": sl,
                "confidence": random.randint(75, 90),
                "rrr": rrr
            })

    # 🔴 Bearish Entry near Swing High
    if price >= last_swing_high * 0.99:
        sl = round(last_swing_high * 1.003, 2)
        tp = round(price * 0.97, 2)
        rrr = calculate_rrr(tp, sl, price, "SELL")
        if rrr >= 1.2:
            results.append({
                "strategy": "WickSwingResistance",
                "type": "BEARISH",
                "price": price,
                "tp": tp,
                "sl": sl,
                "confidence": random.randint(75, 90),
                "rrr": rrr
            })

    return results
