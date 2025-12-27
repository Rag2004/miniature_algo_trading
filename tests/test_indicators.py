from indicators.moving_averages import EMA

def test_ema():
    prices = [10, 11, 12, 13, 14, 15]
    ema = EMA(period=3)

    for p in prices:
        value = ema.update(p)
        print(f"Price={p}, EMA={value}")

if __name__ == "__main__":
    test_ema()
