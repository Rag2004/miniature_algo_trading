# from engine.backtest_engine import BacktestEngine


# def main():
#     print("=" * 70)
#     print("MINI ALGORITHMIC TRADING SYSTEM — EXECUTION TRACE")
#     print("=" * 70)

#     print("\n[1] Initialising system components...")
#     engine = BacktestEngine(
#         csv_path="data/market_data.csv",
#         symbol="BANKNIFTY"
#     )

#     print("    ✔ Market data feed ready")
#     print("    ✔ EMA crossover strategy loaded")
#     print("    ✔ Execution engine initialised")
#     print("    ✔ Risk manager active")
#     print("    ✔ Analytics configured")

#     print("\n[2] Running backtest...\n")
#     summary = engine.run()

#     print("\n[3] TRADE-BY-TRADE EXECUTION TRACE")
#     print("-" * 70)

#     for sid, trades in summary["trades"].items():
#         print(f"\nStrategy: {sid}")
#         print("-" * 70)

#         open_trade = None

#         for trade in trades:
#             if trade.side == "BUY":
#                 open_trade = trade
#                 print(
#                     f"BUY  → Time: {trade.timestamp} | "
#                     f"Price: {trade.price:.2f} | "
#                     f"Qty: {trade.quantity}"
#                 )

#             elif trade.side == "SELL" and open_trade:
#                 pnl = (trade.price - open_trade.price) * trade.quantity
#                 print(
#                     f"SELL → Time: {trade.timestamp} | "
#                     f"Price: {trade.price:.2f} | "
#                     f"Qty: {trade.quantity} | "
#                     f"PnL: {pnl:.2f}"
#                 )
#                 print("-" * 70)
#                 open_trade = None

#     # 🔴 NEW SECTION — SKIPPED TRADES
#     print("\n[4] SKIPPED TRADES (BLOCKED BY RISK MANAGER)")
#     print("-" * 70)

#     if not summary["skipped_trades"]:
#         print("No trades were skipped by risk rules.")
#     else:
#         for skip in summary["skipped_trades"]:
#             print(
#                 f"SKIPPED → Time: {skip['timestamp']} | "
#                 f"Strategy: {skip['strategy_id']} | "
#                 f"Side: {skip['side']} | "
#                 f"Price: {skip['price']:.2f} | "
#                 f"Reason: {skip['reason']}"
#             )

#     print("\n[5] FINAL POSITION SUMMARY")
#     print("-" * 70)

#     for sid, position in summary["positions"].items():
#         print(f"Strategy        : {sid}")
#         print(f"Final Quantity  : {position.quantity}")
#         print(f"Avg Price      : {position.avg_price:.2f}")
#         print(f"Realised PnL   : {position.realised_pnl:.2f}")
#         print("-" * 70)

#     print("\n[6] OUTPUT FILES GENERATED")
#     print("    ✔ output_trades.csv")
#     print("    ✔ output_metrics.csv")

#     print("\n[7] Backtest completed successfully ✅")
#     print("=" * 70)


# if __name__ == "__main__":
#     main()
from data.feed import MarketDataFeed

from strategies.ema_crossover import EMACrossoverStrategy
from strategies.mean_reversion import MeanReversionStrategy
from strategies.opening_range_breakout import OpeningRangeBreakoutStrategy

from risk.risk_manager import RiskManager
from execution.execution_engine import ExecutionEngine
from analytics.metrics import Analytics
from engine.backtest_engine import BacktestEngine


def main():
    print("=" * 80)
    print("MINI ALGORITHMIC TRADING SYSTEM — BACKTEST")
    print("=" * 80)

    print("\n[1] Initializing system components...")

    # ------------------------------------------------------------
    # Market Data Feed
    # ------------------------------------------------------------
    data_feed = MarketDataFeed(
        csv_path="data/market_data.csv",
        symbol="NIFTY"
    )
    data_feed.load()

    # ------------------------------------------------------------
    # Strategies (FINAL 3 — NO time_exit)
    # ------------------------------------------------------------
    strategies = [
        EMACrossoverStrategy(symbol="NIFTY"),
        MeanReversionStrategy(symbol="NIFTY"),
        OpeningRangeBreakoutStrategy(symbol="NIFTY"),
    ]

    # ------------------------------------------------------------
    # Risk Manager
    # ------------------------------------------------------------
    risk_manager = RiskManager(
        max_position_size=5000,
        max_loss_per_strategy=-100000000.0,
        max_profit_per_strategy=500000000.0,
        default_quantity=5
    )

    # ------------------------------------------------------------
    # Execution Engine
    # ------------------------------------------------------------
    execution_engine = ExecutionEngine()

    # ------------------------------------------------------------
    # Analytics
    # ------------------------------------------------------------
    analytics = Analytics()

    # ------------------------------------------------------------
    # Backtest Engine
    # ------------------------------------------------------------
    engine = BacktestEngine(
        data_feed=data_feed,
        strategies=strategies,
        risk_manager=risk_manager,
        execution_engine=execution_engine,
        analytics=analytics
    )

    print("    ✔ Market data feed ready")
    print("    ✔ Strategies loaded:", [s.strategy_id for s in strategies])
    print("    ✔ Execution engine initialized")
    print("    ✔ Risk manager active")
    print("    ✔ Analytics configured")

    # ------------------------------------------------------------
    # Run Backtest
    # ------------------------------------------------------------
    print("\n[2] Running backtest...")
    print("=" * 80)
    engine.run()

    # ------------------------------------------------------------
    # Trade-by-Trade Execution Trace
    # ------------------------------------------------------------
    print("\n[3] TRADE-BY-TRADE EXECUTION TRACE")
    print("-" * 80)

    trades_by_strategy = {}
    for trade in analytics.trades:
        trades_by_strategy.setdefault(trade.strategy_id, []).append(trade)

    for strategy_id, trades in trades_by_strategy.items():
        print(f"\n📊 Strategy: {strategy_id}")
        print("-" * 80)

        for trade in trades:
            pnl_str = f" | PnL: {trade.realized_pnl:+.2f}" if trade.realized_pnl != 0 else ""
            print(
                f"{trade.side:4s} → {trade.timestamp} | "
                f"Price: {trade.price:7.2f} | "
                f"Qty: {trade.quantity:+2d}{pnl_str}"
            )

    # ------------------------------------------------------------
    # Skipped Trades
    # ------------------------------------------------------------
    print("\n[4] SKIPPED TRADES (BLOCKED BY RISK MANAGER)")
    print("-" * 80)

    if not analytics.skipped_trades:
        print("✅ No trades were skipped by risk rules.")
    else:
        for skip in analytics.skipped_trades:
            print(
                f"❌ SKIP → {skip['timestamp']} | "
                f"{skip['strategy_id']:20s} | "
                f"{skip['side']:4s} | "
                f"Reason: {skip['reason']}"
            )

    # ------------------------------------------------------------
    # Final Position Summary
    # ------------------------------------------------------------
    print("\n[5] FINAL POSITION SUMMARY")
    print("-" * 80)

    all_positions = execution_engine.get_all_positions()

    if not all_positions:
        print("No open positions")
    else:
        for (strategy_id, symbol), position in all_positions.items():
            print(f"Strategy       : {strategy_id}")
            print(f"Symbol         : {symbol}")
            print(f"Quantity       : {position.quantity}")
            print(f"Average Price  : {position.average_price:.2f}")
            print("-" * 80)

    # ------------------------------------------------------------
    # Strategy PnL Summary
    # ------------------------------------------------------------
    print("\n[6] STRATEGY PnL SUMMARY")
    print("-" * 80)

    for s in strategies:
        pnl = risk_manager.get_strategy_pnl(s.strategy_id)
        blocked = " [BLOCKED]" if risk_manager.is_blocked(s.strategy_id) else ""
        print(f"{s.strategy_id:25s}: {pnl:+10.2f}{blocked}")

    total_realized = sum(risk_manager.strategy_pnl.values())
    print(f"\n{'TOTAL PnL':25s}: {total_realized:+10.2f}")

    # ------------------------------------------------------------
    # Export Reports
    # ------------------------------------------------------------
    print("\n[7] EXPORTING REPORTS...")
    print("-" * 80)

    analytics.export_trades_csv("output_trades.csv")
    analytics.export_skipped_trades_csv("output_skipped_trades.csv")
    analytics.export_metrics_csv(
        "output_metrics.csv",
        strategy_ids=[s.strategy_id for s in strategies]
    )

    print("\n✅ Backtest completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()
