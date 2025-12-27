class EMA:
    """
    Exponential Moving Average (EMA)
    --------------------------------
    Computes EMA incrementally (bar-by-bar),
    suitable for real-time simulation.
    """

    def __init__(self, period: int):
        self.period = period
        self.multiplier = 2 / (period + 1)
        self.value = None
        self.initialized = False
        self.prices = []

    def update(self, price: float):
        """
        Update EMA with latest close price.
        """
        if not self.initialized:
            self.prices.append(price)

            # Initialize EMA using SMA
            if len(self.prices) == self.period:
                self.value = sum(self.prices) / self.period
                self.initialized = True
            return self.value

        # EMA formula
        self.value = (price - self.value) * self.multiplier + self.value
        return self.value
