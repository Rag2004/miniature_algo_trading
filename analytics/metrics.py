
import csv
from typing import List, Dict
from datetime import datetime
from execution.models import Trade


class Analytics:
 
    def __init__(self):
        """Initialize analytics"""
        self.trades: List[Trade] = []
        self.skipped_trades: List[Dict] = []

    def log_trade(self, trade: Trade):
        """
        Log an executed trade
        
        Args:
            trade: Executed trade object
        """
        self.trades.append(trade)

    def log_skipped_trade(
        self,
        timestamp: datetime,
        strategy_id: str,
        symbol: str,
        side: str,
        reason: str,
        current_position: int,
        strategy_pnl: float
    ):
        """
        Log a skipped trade (rejected by risk manager)
        
        Args:
            timestamp: When signal was generated
            strategy_id: Strategy identifier
            symbol: Trading symbol
            side: BUY or SELL
            reason: Why it was skipped
            current_position: Current position quantity
            strategy_pnl: Current strategy PnL
        """
        self.skipped_trades.append({
            'timestamp': timestamp,
            'strategy_id': strategy_id,
            'symbol': symbol,
            'side': side,
            'reason': reason,
            'current_position': current_position,
            'strategy_pnl': strategy_pnl
        })

    def export_trades_csv(self, path: str):
        """
        Export all executed trades to CSV
        
        Args:
            path: Output file path
        """
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                "strategy_id",
                "symbol",
                "side",
                "quantity",
                "price",
                "realized_pnl",
                "reason"
            ])

            for trade in self.trades:
                writer.writerow([
                    trade.timestamp,
                    trade.strategy_id,
                    trade.symbol,
                    trade.side,
                    trade.quantity,
                    trade.price,
                    round(trade.realized_pnl, 2),
                    trade.reason
                ])
        
        print(f"✅ Exported {len(self.trades)} trades to {path}")

    def export_skipped_trades_csv(self, path: str):
        """
        Export all skipped trades to CSV
        
        Args:
            path: Output file path
        """
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",
                "strategy_id",
                "symbol",
                "side",
                "reason",
                "current_position",
                "strategy_pnl"
            ])

            for skip in self.skipped_trades:
                writer.writerow([
                    skip['timestamp'],
                    skip['strategy_id'],
                    skip['symbol'],
                    skip['side'],
                    skip['reason'],
                    skip['current_position'],
                    round(skip['strategy_pnl'], 2)
                ])
        
        print(f"✅ Exported {len(self.skipped_trades)} skipped trades to {path}")

    def calculate_metrics(self, trades: List[Trade], strategy_id: str) -> Dict:
   
    # Only CLOSED trades (exit legs)
        closed_trades = [t for t in trades if t.realized_pnl != 0]

        if not closed_trades:
            return {
                'strategy_id': strategy_id,
                'total_trades': 0,
                'total_pnl': 0.0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0
            }

        total_pnl = sum(t.realized_pnl for t in closed_trades)

        winning_trades = [t for t in closed_trades if t.realized_pnl > 0]
        losing_trades = [t for t in closed_trades if t.realized_pnl < 0]

        win_rate = len(winning_trades) / len(closed_trades)

        avg_win = (
            sum(t.realized_pnl for t in winning_trades) / len(winning_trades)
            if winning_trades else 0.0
        )

        avg_loss = (
            sum(t.realized_pnl for t in losing_trades) / len(losing_trades)
            if losing_trades else 0.0
        )

        return {
            'strategy_id': strategy_id,
            'total_trades': len(closed_trades),   # ✅ FIX
            'total_pnl': round(total_pnl, 2),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': round(win_rate * 100, 2),
            'avg_win': round(avg_win, 2),
            'avg_loss': round(avg_loss, 2)
    }

    def export_metrics_csv(self, path: str, strategy_ids: List[str]):
        """
        Export metrics for all strategies to CSV
        
        Args:
            path: Output file path
            strategy_ids: List of strategy IDs to analyze
        """
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "strategy_id",
                "total_trades",
                "total_pnl",
                "winning_trades",
                "losing_trades",
                "win_rate_%",
                "avg_win",
                "avg_loss"
            ])

            for strategy_id in strategy_ids:
                # Filter trades for this strategy
                strategy_trades = [t for t in self.trades if t.strategy_id == strategy_id]
                metrics = self.calculate_metrics(strategy_trades, strategy_id)
                
                writer.writerow([
                    metrics['strategy_id'],
                    metrics['total_trades'],
                    metrics['total_pnl'],
                    metrics['winning_trades'],
                    metrics['losing_trades'],
                    metrics['win_rate'],
                    metrics['avg_win'],
                    metrics['avg_loss']
                ])
        
        print(f"✅ Exported metrics to {path}")

    def get_summary(self) -> Dict:
        """
        Get analytics summary
        
        Returns:
            Dict with summary statistics
        """
        return {
            'total_trades': len(self.trades),
            'total_skipped': len(self.skipped_trades),
            'trades': self.trades,
            'skipped_trades': self.skipped_trades
        }