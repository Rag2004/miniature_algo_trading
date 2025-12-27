How to Run:-
pip install -r requirements.txt
python3 main.py


What the System Does:-
Loads historical market data from CSV
Processes data bar-by-bar
Runs multiple strategies in parallel
Generates BUY / SELL signals
Applies centralized risk management
Executes trades and tracks PnL
Exports trades and performance metrics


Implemented Strategies:-
EMA Crossover – EMA(10) vs EMA(20)
Mean Reversion – Price vs SMA
Opening Range Breakout (ORB)



Key Assumptions:-
Data timeframe is 1 minute
Market orders only (no limit orders)
Fixed trade quantity
Single instrument (NIFTY)
Strategies don’t manage positions
Risk manager controls execution
PnL is realized only on SELL trades



Output Files:-
output_trades.csv
output_skipped_trades.csv
output_metrics.csv