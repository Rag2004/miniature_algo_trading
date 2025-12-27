
from typing import List, Dict
from data.feed import MarketDataFeed
from strategies.base import BaseStrategy
from risk.risk_manager import RiskManager
from execution.execution_engine import ExecutionEngine
from execution.models import Position
from analytics.metrics import Analytics


class BacktestEngine:
  
    
    def __init__(self, 
                 data_feed: MarketDataFeed,
                 strategies: List[BaseStrategy],
                 risk_manager: RiskManager,
                 execution_engine: ExecutionEngine,
                 analytics: Analytics):
        
        self.data_feed = data_feed
        self.strategies = strategies
        self.risk_manager = risk_manager
        self.execution_engine = execution_engine
        self.analytics = analytics
        
        self.bars_processed = 0
        
    def run(self):
       
        print("=" * 80)
        print("🚀 BACKTEST ENGINE STARTING")
        print("=" * 80)
        print(f"Strategies: {[s.strategy_id for s in self.strategies]}")
        print(f"Total bars: {len(self.data_feed)}")
        print("=" * 80)
        
        # Iterate through each bar
        for bar in self.data_feed:
            self.bars_processed += 1
            
            # Process bar with each strategy
            for strategy in self.strategies:
                # Strategy generates signal (or None)
                signal = strategy.on_bar(bar)
                
                if signal is None:
                    continue
                
                # Signal generated - process it
                self._process_signal(signal, bar.close)
            
            # Progress indicator
            if self.bars_processed % 100 == 0:
                print(f"📊 Processed {self.bars_processed} bars...")
        
        print("=" * 80)
        print(f"✅ BACKTEST COMPLETE - Processed {self.bars_processed} bars")
        print("=" * 80)
        
        # Final summary
        self._print_summary()
    
    def _process_signal(self, signal, current_price: float):
        
        strategy_id = signal.strategy_id
        symbol = signal.symbol
        

        position = self.execution_engine.get_position(strategy_id, symbol)
        

        approved_qty = self.risk_manager.approve(signal, position)
        
        # Step 3: Execute or skip based on approval
        if approved_qty == 0:
            # Trade rejected by risk manager
            self.analytics.log_skipped_trade(
                timestamp=signal.timestamp,
                strategy_id=strategy_id,
                symbol=symbol,
                side=signal.side,
                reason="Risk manager rejected",
                current_position=position.quantity,
                strategy_pnl=self.risk_manager.get_strategy_pnl(strategy_id)
            )
            return
        
        # Step 4: Trade approved - execute it
        # Determine actual quantity based on side
        if signal.side == "BUY":
            quantity = approved_qty
        elif signal.side == "SELL":
            quantity = -approved_qty  # Negative for sells
        else:
            print(f"⚠️  Invalid signal side: {signal.side}")
            return
        
        # Execute the trade
        trade = self.execution_engine.execute_trade(
            strategy_id=strategy_id,
            symbol=symbol,
            quantity=quantity,
            price=current_price,
            timestamp=signal.timestamp,
            signal_reason=signal.reason
        )
        
        if trade:
            # Log successful trade
            self.analytics.log_trade(trade)
            
            # If trade closed a position, update strategy PnL in risk manager
            if trade.realized_pnl != 0:
                self.risk_manager.update_strategy_pnl(strategy_id, trade.realized_pnl)
            
            print(f"✅ TRADE: {signal.side} {abs(quantity)} {symbol} @ {current_price:.2f} "
                  f"[{strategy_id}] - {signal.reason}")
    
    def _print_summary(self):
        """Print final summary"""
        print("\n📈 FINAL POSITIONS:")
        print("-" * 80)
        
        all_positions = self.execution_engine.get_all_positions()
        
        if not all_positions:
            print("No positions")
        else:
            for key, position in all_positions.items():
                unrealized = position.unrealized_pnl
                print(f"  {key}: Qty={position.quantity}, "
                      f"AvgPrice={position.average_price:.2f}, "
                      f"UnrealizedPnL={unrealized:.2f}")
        
        print("\n💰 STRATEGY PnL:")
        print("-" * 80)
        for strategy_id, pnl in self.risk_manager.strategy_pnl.items():
            blocked = " [BLOCKED]" if self.risk_manager.is_blocked(strategy_id) else ""
            print(f"  {strategy_id}: {pnl:.2f}{blocked}")
        
        print("\n📊 ANALYTICS:")
        print("-" * 80)
        print(f"  Total trades executed: {len(self.analytics.trades)}")
        print(f"  Total signals skipped: {len(self.analytics.skipped_trades)}")
        
        # Calculate total PnL
        total_realized = sum(self.risk_manager.strategy_pnl.values())
        total_unrealized = sum(p.unrealized_pnl for p in all_positions.values())
        total_pnl = total_realized + total_unrealized
        
        print(f"\n💵 TOTAL PnL: {total_pnl:.2f}")
        print(f"  Realized: {total_realized:.2f}")
        print(f"  Unrealized: {total_unrealized:.2f}")
        print("=" * 80)