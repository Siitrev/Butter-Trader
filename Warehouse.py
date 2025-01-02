class Warehouse:
    def __init__(self):
        self._level = 1
        self._capacity = 1000
        self._rent_cost = self._capacity / 1000 * 5670 
        
    def upgrade(self) -> bool:
        if self._level < 4:
            self._level += 1
            self._rent_cost = self.capacity / 1000 * 5670 
            return True
        return False
    
    def isUpgradeable(self) -> bool:
        return self._level < 4
    
    @property
    def capacity(self):
        return self._capacity * 2**(self.level - 1)
    
    @property
    def level(self):
        return self._level
    
    @property
    def rent_cost(self):
        return self._rent_cost