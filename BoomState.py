from IMarketState import IMarketState
from Market import Market
from GeometricBrownianMotionStrategy import GeometricBrownianMotionStrategy
import random

class BoomState(IMarketState):
    def __init__(self):
        self.weeks = 0
    
    def onEnter(self):
        market = Market.getInstance()
        sigma = 0.5
        strategy = GeometricBrownianMotionStrategy(5, sigma)
        market.strategy = strategy
    
    def update(self):
        from NormalState import NormalState
        market = Market.getInstance()
        chance = random.random()
        if chance < self.weeks/25:
            market.state = NormalState()
            
        self.weeks += 1