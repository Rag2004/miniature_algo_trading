from engine.backtest_engine import BacktestEngine


def test_backtest_with_pnl():
    engine = BacktestEngine(
        csv_path="data/market_data.csv",
        symbol="BANKNIFTY"
    )

    summary = engine.run()

    print("\n===== BACKTEST RESULT =====")

    print("\nPOSITIONS:")
    for sid, pos in summary["positions"].items():
        print(
            f"Strategy={sid}, Qty={pos.quantity}, "
            f"AvgPrice={pos.avg_price}, RealisedPnL={pos.realised_pnl}"
        )

    print("\nUNREALISED PnL:")
    for sid, pnl in summary["unrealised_pnl"].items():
        print(f"{sid}: {pnl}")

    print("\nTRADES:")
    for sid, trades in summary["trades"].items():
        print(f"{sid}: {len(trades)} trades")


if __name__ == "__main__":
    test_backtest_with_pnl()
