# from datetime import time
# from typing import Optional
# from data.bar import Bar
# from core.signal import Signal
# from .base import BaseStrategy


# class OpeningRangeBreakoutStrategy(BaseStrategy):
#     """
#     First 15 minutes high/low breakout.
#     One trade per day.
#     """

#     def __init__(self, symbol="NIFTY"):
#         super().__init__("opening_range", symbol)
#         self.range_high = None
#         self.range_low = None
#         self.range_complete = False
#         self.trade_taken = False

#     def on_bar(self, bar: Bar) -> Optional[Signal]:
#         t = bar.timestamp.time()

#         if t <= time(9, 30):
#             self.range_high = max(self.range_high or bar.high, bar.high)
#             self.range_low = min(self.range_low or bar.low, bar.low)
#             return None

#         if not self.range_complete:
#             self.range_complete = True

#         if self.trade_taken:
#             return None

#         if bar.close > self.range_high and self.can_buy():
#             self.trade_taken = True
#             return Signal(
#                 self.strategy_id, self.symbol, "BUY",
#                 bar.timestamp, "ORB breakout high"
#             )

#         if bar.close < self.range_low and self.can_buy():
#             self.trade_taken = True
#             return Signal(
#                 self.strategy_id, self.symbol, "SELL",
#                 bar.timestamp, "ORB breakout low"
#             )

#         return None

#     def reset(self):
#         super().reset()
#         self.range_high = None
#         self.range_low = None
#         self.range_complete = False
#         self.trade_taken = False
from datetime import time
from typing import Optional
from data.bar import Bar
from core.signal import Signal
from .base import BaseStrategy


class OpeningRangeBreakoutStrategy(BaseStrategy):

    def __init__(self, symbol="NIFTY"):
        super().__init__("opening_range", symbol)
        self.or_high = None
        self.or_low = None
        self.range_done = False
        self.in_position = False   # 🔑

    def on_bar(self, bar: Bar):
        t = bar.timestamp.time()

        if not self.range_done:
            self.or_high = bar.high if self.or_high is None else max(self.or_high, bar.high)
            self.or_low = bar.low if self.or_low is None else min(self.or_low, bar.low)

            if t >= time(9, 30):
                self.range_done = True
            return None

        # BUY breakout
        if not self.in_position and bar.close > self.or_high:
            self.in_position = True
            return Signal(
                self.strategy_id, self.symbol, "BUY",
                bar.timestamp, "ORB breakout high"
            )

        # SELL breakdown
        if self.in_position and bar.close < self.or_low:
            self.in_position = False
            return Signal(
                self.strategy_id, self.symbol, "SELL",
                bar.timestamp, "ORB breakdown low"
            )

        return None
