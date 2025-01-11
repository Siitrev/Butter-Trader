import numpy as np
from IPriceStrategy import IPriceStrategy

class MeanRevertingStrategy(IPriceStrategy):  
    def __init__(self, mu=40.0, theta=10, sigma=0.3, dt=1/52):        
        self.mu = mu  
        self.theta = theta  
        self.sigma = sigma  
        self.dt = dt  
  
    def calculatePrice(self, prev_price):  
        # delta_price = self.theta * (self.mu - prev_price) * self.dt + self.sigma * np.random.normal(0, np.sqrt(self.dt))
        
        # max_change = 1 / prev_price
        # delta_price = np.clip(delta_price, -max_change, max_change)
            
        # new_price = prev_price + delta_price  
  
        # return max(new_price, 0.1)
        diff = self.mu - prev_price
        
        rand_drift = np.random.normal(13, 5)
        drift = rand_drift if diff > 0 else -rand_drift
        
        mean_reversion = self.theta * diff * self.dt
        
        stochastic_term = drift * self.dt + self.sigma * np.random.normal(0, np.sqrt(self.dt))

        delta_price = mean_reversion + stochastic_term
        
        # max_change = 0.01 * old_price  
        # delta_price = np.clip(delta_price, -max_change, max_change)

        new_price = prev_price + delta_price

        # Return the final smoothed price
        return max(new_price, 0.1)