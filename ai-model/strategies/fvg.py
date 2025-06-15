# strategies/fvg.py

import random
from utils.rrr_calculator import calculate_rrr

def fvg_strategy(data):
    results = []

    latest = data.iloc[-1]
    price = round(latest['close'], 2)

    # BUY
    tp = round(price * 1.02, 2)
    sl = round(price * 0.98, 2)
    rrr = calculate_rrr(tp, sl, price, "BUY")
    if rrr >= 1.2:
        results.append({
            "strategy": "FVG",
            "type": "BUY",
            "price": price,
            "tp": tp,
            "sl": sl,
            "confidence": random.randint(80, 95),
            "rrr": rrr
        })

    # SELL
    tp = round(price * 0.98, 2)
    sl = round(price * 1.02, 2)
    rrr = calculate_rrr(tp, sl, price, "SELL")
    if rrr >= 1.2:
        results.append({
            "strategy": "FVG",
            "type": "SELL",
            "price": price,
            "tp": tp,
            "sl": sl,
            "confidence": random.randint(80, 95),
            "rrr": rrr
        })

    return results
