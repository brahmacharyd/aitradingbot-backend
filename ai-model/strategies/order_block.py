import random
from utils.rrr_calculator import calculate_rrr

def order_block_strategy(data):
    results = []

    latest = data.iloc[-1]
    price = round(latest['close'], 2)

    bullish = {}
    bearish = {}

    # BEARISH
    tp_bear = round(price * 0.97, 2)
    sl_bear = round(price * 1.01, 2)
    rrr_bear = calculate_rrr(tp_bear, sl_bear, price, "SELL")
    if rrr_bear >= 1.2:
        bearish = {
            "strategy": "OrderBlock",
            "type": "BEARISH",
            "price": price,
            "tp": tp_bear,
            "sl": sl_bear,
            "confidence": random.randint(75, 90),
            "rrr": rrr_bear
        }

    # BULLISH
    tp_bull = round(price * 1.03, 2)
    sl_bull = round(price * 0.99, 2)
    rrr_bull = calculate_rrr(tp_bull, sl_bull, price, "BUY")
    if rrr_bull >= 1.2:
        bullish = {
            "strategy": "OrderBlock",
            "type": "BULLISH",
            "price": price,
            "tp": tp_bull,
            "sl": sl_bull,
            "confidence": random.randint(75, 90),
            "rrr": rrr_bull
        }

    # Decision filtering
    if bullish and not bearish:
        results.append(bullish)
    elif bearish and not bullish:
        results.append(bearish)
    elif bullish and bearish:
        # If both exist, choose stronger one, or both if close (conflict)
        if abs(bullish["confidence"] - bearish["confidence"]) <= 5:
            results.extend([bullish, bearish])  # mark as conflict
        else:
            results.append(bullish if bullish["confidence"] > bearish["confidence"] else bearish)

    return results
