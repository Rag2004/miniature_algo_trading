
from typing import Optional
from datetime import time
from data.bar import Bar
from core.signal import Signal
from .base import BaseStrategy


class TimeExitStrategy(BaseStrategy):
    
    
    def __init__(self, strategy_id: str = "time_exit", symbol: str = "NIFTY",
                 entry_time: time = time(9, 30), exit_time: time = time(15, 15)):
       
        super().__init__(strategy_id, symbol)
        self.entry_time = entry_time
        self.exit_time = exit_time
        
        # Track if we've already signaled today
        self.last_entry_date = None
        self.last_exit_date = None
        
    def on_bar(self, bar: Bar) -> Optional[Signal]:
       
        self.bars_processed += 1
        
        current_time = bar.timestamp.time()
        current_date = bar.timestamp.date()
        
        # Check for entry signal
        if current_time >= self.entry_time and self.last_entry_date != current_date:
            self.last_entry_date = current_date
            return Signal(
                strategy_id=self.strategy_id,
                symbol=self.symbol,
                side="BUY",
                timestamp=bar.timestamp,
                reason=f"Entry time reached: {self.entry_time}"
            )
        
        # Check for exit signal
        if current_time >= self.exit_time and self.last_exit_date != current_date:
            self.last_exit_date = current_date
            return Signal(
                strategy_id=self.strategy_id,
                symbol=self.symbol,
                side="SELL",
                timestamp=bar.timestamp,
                reason=f"Exit time reached: {self.exit_time}"
            )
        
        return None
    
    def reset(self):
        """Reset strategy state"""
        super().reset()
        self.last_entry_date = None
        self.last_exit_date = None