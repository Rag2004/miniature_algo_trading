
import numpy as np
from typing import List, Optional
from data.bar import Bar
from core.signal import Signal
from .base import BaseStrategy


class MeanReversionStrategy(BaseStrategy):

    def __init__(self, symbol="NIFTY", period=20):
        super().__init__("mean_reversion", symbol)
        self.period = period
        self.prices = []
        self.in_position = False   # 🔑

    def on_bar(self, bar: Bar):
        self.prices.append(bar.close)

        if len(self.prices) < self.period:
            return None

        sma = np.mean(self.prices[-self.period:])
        price = bar.close

        # BUY once
        if not self.in_position and price < sma:
            self.in_position = True
            return Signal(
                self.strategy_id, self.symbol, "BUY",
                bar.timestamp, "Mean reversion entry"
            )

        # SELL once
        if self.in_position and price >= sma:
            self.in_position = False
            return Signal(
                self.strategy_id, self.symbol, "SELL",
                bar.timestamp, "Mean reversion exit"
            )

        return None

