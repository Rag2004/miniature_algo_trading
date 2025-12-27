
from typing import Dict, Optional
from datetime import datetime
from execution.models import Trade, Position


class ExecutionEngine:
    

    def __init__(self):
        """Initialize execution engine"""
        # Key: (strategy_id, symbol) -> Position
        self.positions: Dict[tuple, Position] = {}
        
        # All executed trades
        self.trades: list = []

    def execute_trade(
        self, 
        strategy_id: str,
        symbol: str,
        quantity: int,  # Signed: positive=BUY, negative=SELL
        price: float,
        timestamp: datetime,
        signal_reason: str = ""
    ) -> Optional[Trade]:
  
        position = self.get_position(strategy_id, symbol)
        
        # Determine side and absolute quantity
        if quantity > 0:
            side = "BUY"
            abs_qty = quantity
        elif quantity < 0:
            side = "SELL"
            abs_qty = abs(quantity)
        else:
            # Zero quantity - shouldn't happen
            return None
        
        # Calculate realized PnL (only for position-closing trades)
        realized_pnl = 0.0
        
        if side == "BUY":
            # Buying - update position
            position.buy(abs_qty, price)
            
        elif side == "SELL":
            # Selling - calculate PnL and update position
            realized_pnl = position.sell(abs_qty, price)
        
        # Create trade record
        trade = Trade(
            strategy_id=strategy_id,
            symbol=symbol,
            side=side,
            quantity=quantity,  # Keep signed
            price=price,
            timestamp=timestamp,
            realized_pnl=realized_pnl,
            reason=signal_reason
        )
        
        # Record trade
        self.trades.append(trade)
        
        return trade

    def get_position(self, strategy_id: str, symbol: str) -> Position:
       
        key = (strategy_id, symbol)
        
        if key not in self.positions:
            self.positions[key] = Position(
                strategy_id=strategy_id,
                symbol=symbol
            )
        
        return self.positions[key]

    def get_all_positions(self) -> Dict[tuple, Position]:
        return self.positions.copy()

    def calculate_unrealized_pnl(self, strategy_id: str, symbol: str, current_price: float) -> float:
      
        position = self.get_position(strategy_id, symbol)
        return position.calculate_unrealized_pnl(current_price)