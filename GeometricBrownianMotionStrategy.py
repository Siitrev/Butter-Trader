from IPriceStrategy import IPriceStrategy
import numpy as np

class GeometricBrownianMotionStrategy(IPriceStrategy):
    def __init__(self, mu=0.05, sigma=0.2, dt=1/52):
        """
        :param mu: średnia stopa zwrotu (drift)
        :param sigma: zmienność (volatility)
        :param dt: krok czasu (np. 1/252 odpowiada jednemu dniu w roku handlowym)
        """
        self.mu = mu
        self.sigma = sigma
        self.dt = dt
        
    def calculatePrice(self, prev_price):
        epsilon = np.random.normal()
        delta_price = (self.mu - 0.5 * self.sigma ** 2) * self.dt + self.sigma * np.sqrt(self.dt) * epsilon
        
        max_delta = 1 / prev_price
        delta_price = np.clip(delta_price, -max_delta, max_delta)
        
        new_price = prev_price * np.exp(delta_price)
        return max(new_price, 0.1)