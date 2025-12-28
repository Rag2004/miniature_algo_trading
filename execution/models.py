"""
Position and Trade models
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Trade:
    """Record of an executed trade"""
    strategy_id: str
    symbol: str
    side: str            # BUY / SELL
    quantity: int        # Signed: positive for BUY, negative for SELL
    price: float
    timestamp: datetime
    realized_pnl: float = 0.0  # PnL realized by this trade (if closing position)
    reason: str = ""     # Signal reason


@dataclass
class Position:
    
    strategy_id: str
    symbol: str
    quantity: int = 0
    average_price: float = 0.0
    
    def buy(self, qty: int, price: float):
        if self.quantity < 0:
            # Closing short position
            if qty >= abs(self.quantity):
                # Closing entire short or flipping to long
                self.quantity += qty
                if self.quantity > 0:
                    self.average_price = price
                else:
                    self.average_price = 0.0
            else:
                # Partially closing short
                self.quantity += qty
        else:
            # Adding to long or opening new long
            total_cost = self.average_price * self.quantity + price * qty
            self.quantity += qty
            self.average_price = total_cost / self.quantity if self.quantity > 0 else 0.0
    
    def sell(self, qty: int, price: float) -> float:
        
        realized_pnl = 0.0
        
        if self.quantity > 0:
            # Closing long position
            close_qty = min(qty, self.quantity)
            realized_pnl = (price - self.average_price) * close_qty
            self.quantity -= qty
            
            if self.quantity <= 0:
                # Closed entire long, possibly went short
                if self.quantity < 0:
                    # Flipped to short
                    self.average_price = price
                else:
                    self.average_price = 0.0
        else:
            # Opening or adding to short position
            total_value = abs(self.average_price * self.quantity) + price * qty
            self.quantity -= qty
            self.average_price = total_value / abs(self.quantity) if self.quantity != 0 else 0.0
        
        return realized_pnl
    
    @property
    def unrealized_pnl(self) -> float:
        """Calculate unrealized PnL (needs current price, set externally)"""
        # This will be calculated by passing current price when needed
        return 0.0
    
    def calculate_unrealized_pnl(self, current_price: float) -> float:
        if self.quantity == 0:
            return 0.0
        return (current_price - self.average_price) * self.quantity