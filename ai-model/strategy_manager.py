# ai-model/strategy_manager.py

from strategies import fvg, order_block, rsi_combo,swing_strategy,smc_strategy

def apply_strategies(symbol, data):
    all_signals = []

    for strategy_func in [
        fvg.fvg_strategy,
        order_block.order_block_strategy,
        rsi_combo.rsi_strategy, # <- Add this line
       swing_strategy.swing_strategy,  # <- Add this line
       smc_strategy.smc_strategy

    ]:
        signals = strategy_func(data)
        for signal in signals:
            signal["symbol"] = symbol
            all_signals.append(signal)

    return all_signals
