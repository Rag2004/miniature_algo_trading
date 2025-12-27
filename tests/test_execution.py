from execution.execution_engine import ExecutionEngine

def test_execution_engine():
    engine = ExecutionEngine()

    prices = [10, 11, 12, 11]
    signals = [None, None, "BUY", "SELL"]

    for price, signal in zip(prices, signals):
        if signal:
            engine.execute(signal, price)

    summary = engine.summary()
    print("SUMMARY:", summary)

if __name__ == "__main__":
    test_execution_engine()
