
from abc import ABC, abstractmethod
from typing import Optional
from data.bar import Bar
from core.signal import Signal


class BaseStrategy(ABC):
    """
    Base class for all strategies.
    Enforces:
    - One position at a time
    - No short selling
    """

    def __init__(self, strategy_id: str, symbol: str):
        self.strategy_id = strategy_id
        self.symbol = symbol

        self.position_qty = 0
        self.bars_processed = 0

    def can_buy(self) -> bool:
        return self.position_qty == 0

    def can_sell(self) -> bool:
        return self.position_qty > 0

    def on_trade_executed(self, side: str, qty: int):
        if side == "BUY":
            self.position_qty += qty
        elif side == "SELL":
            self.position_qty -= qty

    @abstractmethod
    def on_bar(self, bar: Bar) -> Optional[Signal]:
        pass

    def reset(self):
        self.position_qty = 0
        self.bars_processed = 0
