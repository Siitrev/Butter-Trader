from IMarketState import IMarketState
from Market import Market
from MeanRevertingStrategy import MeanRevertingStrategy

class NormalState(IMarketState):        
    def onEnter(self):
        market = Market.getInstance()
        strategy = MeanRevertingStrategy(market.base_price)
        market.strategy = strategy
    
    def update(self):
        pass
                        
            
        
                