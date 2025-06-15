def calculate_rrr(tp, sl, price, order_type):
    try:
        if order_type.upper() == "BUY":
            risk = price - sl
            reward = tp - price
        else:
            risk = sl - price
            reward = price - tp

        if risk <= 0:
            return 0
        return round(reward / risk, 2)
    except:
        return 0
