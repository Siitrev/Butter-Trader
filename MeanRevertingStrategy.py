import numpy as np
from IPriceStrategy import IPriceStrategy

class MeanRevertingStrategy(IPriceStrategy):  
    def __init__(self, mu=10.0, theta=0.1, sigma=0.2, dt=1):  
        self.initial_mu = mu  
        self.initial_theta = theta  
        self.initial_sigma = sigma  
          
        self.mu = mu  
        self.theta = theta  
        self.sigma = sigma  
        self.dt = dt  
        self.prev_price = None  
  
    def calculatePrice(self, current_price):  
        if self.prev_price is None:  
            self.prev_price = current_price  
  
        epsilon = np.random.normal()  
        delta_price = self.theta * (self.mu - self.prev_price) * self.dt + self.sigma * epsilon * np.sqrt(self.dt)  
        new_price = self.prev_price + delta_price  
  
        self.prev_price = new_price  
  
        return max(new_price, 0.1)