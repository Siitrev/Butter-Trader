from IMarketState import IMarketState
from Market import Market
from GeometricBrownianMotionStrategy import GeometricBrownianMotionStrategy
import random

class BoomState(IMarketState):
    def __init__(self):
        self.days = 1
    
    def onEnter(self):
        market = Market.getInstance()
        sigma = random.uniform(0.1, 0.3)
        strategy = GeometricBrownianMotionStrategy(0.07, sigma, 1/10)
        market.setStrategy(strategy)
    
    def update(self):
        from NormalState import NormalState
        market = Market.getInstance()
        chance = random.random()
        if chance < 0.05 + (self.days/20):
            market.setState(NormalState())
            
        self.days += 1