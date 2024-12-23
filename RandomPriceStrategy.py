from IPriceStrategy import IPriceStrategy

class RandomPriceStrategy(IPriceStrategy):
    def updatePrice(self, current_price):
        return super().updatePrice(current_price)