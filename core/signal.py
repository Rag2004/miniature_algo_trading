
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Signal:
   
    strategy_id: str
    symbol: str
    side: str  # "BUY" or "SELL"
    timestamp: datetime
    reason: str = ""
    
    def __post_init__(self):
        """Validate signal fields"""
        if self.side not in ["BUY", "SELL"]:
            raise ValueError(f"Invalid side: {self.side}. Must be BUY or SELL")
    
    def __repr__(self):
        return (f"Signal(strategy={self.strategy_id}, symbol={self.symbol}, "
                f"side={self.side}, reason='{self.reason}')")