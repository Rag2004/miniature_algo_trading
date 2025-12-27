from data.feed import MarketDataFeed


def test_market_data_feed():
    feed = MarketDataFeed(
        csv_path="data\market_data.csv",
        symbol="NIFTYBANK"
    )

    count = 0
    while feed.has_next():
        bar = feed.get_next_bar()
        count += 1

        # Basic sanity checks
        assert bar["high"] >= bar["low"]
        assert bar["timestamp"] is not None

    print(f"Total bars processed: {count}")


if __name__ == "__main__":
    test_market_data_feed()
