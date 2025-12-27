import numpy as np
from data.bar import Bar
from core.signal import Signal
from .base import BaseStrategy


class EMACrossoverStrategy(BaseStrategy):
    

    def __init__(self, symbol="NIFTY", fast=10, slow=20):
        super().__init__("ema_crossover", symbol)
        self.fast = fast
        self.slow = slow

        self.prices = []
        self.prev_fast = None
        self.prev_slow = None
        self.in_position = False

    def _ema(self, prices, period):
        alpha = 2 / (period + 1)
        ema = prices[0]
        for price in prices[1:]:
            ema = alpha * price + (1 - alpha) * ema
        return ema

    def on_bar(self, bar: Bar):
        self.prices.append(bar.close)

        if len(self.prices) < self.slow + 1:
            return None

        fast_ema = self._ema(self.prices[-self.fast:], self.fast)
        slow_ema = self._ema(self.prices[-self.slow:], self.slow)

        signal = None

        if self.prev_fast is not None:

            # BUY once
            if (
                not self.in_position and
                self.prev_fast <= self.prev_slow and
                fast_ema > slow_ema
            ):
                self.in_position = True
                signal = Signal(
                    self.strategy_id, self.symbol, "BUY",
                    bar.timestamp, "EMA bullish crossover"
                )

            # SELL once
            elif (
                self.in_position and
                self.prev_fast >= self.prev_slow and
                fast_ema < slow_ema
            ):
                self.in_position = False
                signal = Signal(
                    self.strategy_id, self.symbol, "SELL",
                    bar.timestamp, "EMA bearish crossover"
                )

        self.prev_fast = fast_ema
        self.prev_slow = slow_ema
        return signal
