class EMA:
    
    def __init__(self, period: int):
        self.period = period
        self.multiplier = 2 / (period + 1)
        self.value = None
        self.initialized = False
        self.prices = []

    def update(self, price: float):
       
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
