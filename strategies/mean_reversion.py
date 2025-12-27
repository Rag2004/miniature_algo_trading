# import numpy as np
# from typing import List, Optional
# from data.bar import Bar
# from core.signal import Signal
# from .base import BaseStrategy


# class MeanReversionStrategy(BaseStrategy):
#     """
#     BUY when price is far below SMA
#     SELL when price reverts to SMA
#     """

#     def __init__(self, symbol="NIFTY", period=20, threshold=30):
#         super().__init__("mean_reversion", symbol)
#         self.period = period
#         self.threshold = threshold
#         self.prices: List[float] = []

#     def on_bar(self, bar: Bar) -> Optional[Signal]:
#         self.prices.append(bar.close)
#         self.bars_processed += 1

#         if len(self.prices) < self.period:
#             return None

#         sma = np.mean(self.prices[-self.period:])

#         if bar.close < sma - self.threshold and self.can_buy():
#             return Signal(
#                 self.strategy_id, self.symbol, "BUY",
#                 bar.timestamp, "Price below SMA"
#             )

#         if bar.close >= sma and self.can_sell():
#             return Signal(
#                 self.strategy_id, self.symbol, "SELL",
#                 bar.timestamp, "Mean reversion exit"
#             )

#         return None
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

