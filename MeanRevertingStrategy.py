import numpy as np
from IPriceStrategy import IPriceStrategy

class MeanRevertingStrategy(IPriceStrategy):  
    def __init__(self, mu=10.0, theta=0.00454, sigma=0.00908, dt=1/52):  
        self.initial_mu = mu  
        self.initial_theta = theta  
        self.initial_sigma = sigma  
          
        self.mu = mu  
        self.theta = theta  
        self.sigma = sigma  
        self.dt = dt  
  
    def calculatePrice(self, prev_price):  
        epsilon = np.random.normal()  
        delta_price = self.theta * (self.mu - prev_price) * self.dt + self.sigma * epsilon * np.sqrt(self.dt)  
        new_price = prev_price + delta_price  
  
        return max(new_price, 0.1)