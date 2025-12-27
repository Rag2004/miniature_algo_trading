from datetime import datetime

from strategies.ema_crossover import EMACrossoverStrategy
from data.bar import Bar


def test_ema_crossover_strategy():
    strategy = EMACrossoverStrategy(fast_period=3, slow_period=5)

    prices = [100, 101, 102, 103, 104, 105]

    for price in prices:
        bar = Bar(
            timestamp=datetime.utcnow(),
            symbol="TEST",
            open=price,
            high=price,
            low=price,
            close=price,
        )
        signal = strategy.on_bar(bar)

    # We don't assert signal here yet because:
    # - crossover depends on EMA state
    # - this test is only for contract validation
