
from typing import Dict, Optional
from core.signal import Signal
from execution.models import Position


class RiskManager:
   
    
    def __init__(self, 
                 max_position_size: int = 1,
                 max_loss_per_strategy: float = -20000.0,
                 max_profit_per_strategy: float = 50000.0,
                 default_quantity: int = 1):
      
        self.max_position_size = max_position_size
        self.max_loss_per_strategy = max_loss_per_strategy
        self.max_profit_per_strategy = max_profit_per_strategy
        self.default_quantity = default_quantity
        
   
        self.strategy_pnl: Dict[str, float] = {}
        
        # Track blocked strategies (hit limits)
        self.blocked_strategies: set = set()
        
    def approve(self, signal: Signal, position: Position) -> int:
       
        strategy_id = signal.strategy_id
        
        # Initialize strategy PnL tracking if needed
        if strategy_id not in self.strategy_pnl:
            self.strategy_pnl[strategy_id] = 0.0
        
        # Rule 1: Check if strategy is blocked due to limits
        if strategy_id in self.blocked_strategies:
            return 0
        
        # Rule 2: Check strategy PnL limits
        current_pnl = self.strategy_pnl[strategy_id]
        
        if current_pnl <= self.max_loss_per_strategy:
            self.blocked_strategies.add(strategy_id)
            print(f"❌ Strategy {strategy_id} BLOCKED: Hit max loss (PnL: {current_pnl:.2f})")
            return 0
        
        if current_pnl >= self.max_profit_per_strategy:
            self.blocked_strategies.add(strategy_id)
            print(f"❌ Strategy {strategy_id} BLOCKED: Hit max profit (PnL: {current_pnl:.2f})")
            return 0
        
        # Rule 3: Position size limits
        current_qty = position.quantity
        
        if signal.side == "BUY":
            # Trying to buy
            if current_qty >= self.max_position_size:
                # Already at max long position
                return 0
            
            # Approve default quantity, but don't exceed max position
            approved_qty = min(self.default_quantity, self.max_position_size - current_qty)
            return approved_qty
        
        elif signal.side == "SELL":
            # Trying to sell
            if current_qty <= -self.max_position_size:
                # Already at max short position
                return 0
            
            # For SELL, quantity is negative direction
            # Approve default quantity, but don't exceed max position
            approved_qty = min(self.default_quantity, self.max_position_size + current_qty)
            return approved_qty
        
        # Invalid signal side (shouldn't happen)
        return 0
    
    def update_strategy_pnl(self, strategy_id: str, realized_pnl: float):
       
        if strategy_id not in self.strategy_pnl:
            self.strategy_pnl[strategy_id] = 0.0
        
        self.strategy_pnl[strategy_id] += realized_pnl
    
    def get_strategy_pnl(self, strategy_id: str) -> float:
        """Get current PnL for a strategy"""
        return self.strategy_pnl.get(strategy_id, 0.0)
    
    def is_blocked(self, strategy_id: str) -> bool:
        """Check if strategy is blocked"""
        return strategy_id in self.blocked_strategies
    
    def reset(self):
        """Reset risk manager state"""
        self.strategy_pnl = {}
        self.blocked_strategies = set()
    
    def get_summary(self) -> Dict:
        """Get risk summary"""
        return {
            'strategy_pnl': self.strategy_pnl.copy(),
            'blocked_strategies': list(self.blocked_strategies),
            'max_position_size': self.max_position_size,
            'max_loss_per_strategy': self.max_loss_per_strategy,
            'max_profit_per_strategy': self.max_profit_per_strategy
        }