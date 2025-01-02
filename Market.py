from typing import TYPE_CHECKING
import matplotlib.ticker
import pygame as py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib
import numpy as np

if TYPE_CHECKING:
    from IMarketState import IMarketState
    from UIObserver import UIObserver
    from IPriceStrategy import IPriceStrategy

class Market:
    __instance = None
    
    @staticmethod
    def getInstance():
        if Market.__instance is None:
            Market()
        return Market.__instance
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value: float):
        self.prev_price = self._price
        self._price = value
        change = self._price - self.prev_price
        self.notifyAll({"butter_price_label" : str(value), "price_change_label" : str(change)})
        
    @property
    def base_price(self):
        return self._base_price
    
    @base_price.setter
    def base_price(self, value: float):
        self._base_price = value
        
    @property
    def prev_price(self):
        return self._prev_price
    
    @prev_price.setter
    def prev_price(self, value: float):
        self._prev_price = value
        
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, state: float):
        self._state = state
        print(f"Zmieniono stan na: {state}")
        self._state.onEnter()
        
    @property
    def strategy(self):
        return self._strategy
    
    @strategy.setter
    def strategy(self, strategy: float):
        self._strategy = strategy
    
    def __init__(self):
        if Market.__instance is not None:
            raise Exception("Instance of that object already exists")
        else:
            Market.__instance = self
        self._price = 40.0
        self.__history = []
        self.__min_price = 35.0
        self.__max_price = 45.0
        self._prev_price = 40.0
        self._base_price = 40.0
        self.__observers: list["UIObserver"] = []
        self._strategy: "IPriceStrategy" = None
        self._state: "IMarketState" = None
        
    def attach(self, observer):
        self.__observers.append(observer)
        
    def detach(self, observer):
        self.__observers.remove(observer)
        
    def notifyAll(self, ui_elements: dict[str, str]):
        for object_id, value in ui_elements.items():
            for observer in self.__observers:
                observer.update(object_id, value)
            
    def updatePrice(self):
        self.price = self.strategy.calculatePrice(self.prev_price)
        
    def update(self, week):
        self.state.update()
        self.updatePrice()
        self.__history = [x for x in self.__history[-9:]]
        self.__history.append((week, self._price))
        
        current_min_price = min(self.__history, key=lambda x: x[1])[1]
        current_max_price = max(self.__history, key=lambda x: x[1])[1]
        
        if current_max_price > self.__max_price:
            self.__max_price = current_max_price
        
        if current_min_price < self.__min_price:
            self.__min_price = current_min_price
        
    def createChart(self):
        matplotlib.use('Agg')
        prices = []
        weeks = []
        for week, price in self.__history:
            prices.append(price)
            weeks.append(week)
        
        latest_week = 10
        oldest_week = 0
        
        if weeks[-1] > 10:
            latest_week = weeks[-1] 
            oldest_week = weeks[0]
        
        fig, ax = plt.subplots(figsize=(9, 4), dpi=100)
 
        ax.plot(weeks, prices, marker='o', linestyle='-', color='blue', linewidth=2)  
    
        ax.set_ylim(self.__min_price, self.__max_price)  
    
        ax.autoscale(enable=False, axis='y')  
    
        ax.set_yticks(np.arange(self.__min_price, self.__max_price + 1, 1))  
        ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%d'))  
    
        ax.grid(True, which='major', axis='y', linestyle='--', linewidth=0.5)  
    
        ax.set_xlabel("Czas (Tygodnie)")  
        ax.set_ylabel("Cena")  
        
        plt.xticks(np.arange(oldest_week, latest_week + 1, 1))
        
        canvas = FigureCanvasAgg(fig)
        canvas.draw()
        raw_data = canvas.tostring_argb()
        width, height = canvas.get_width_height()
        surface = py.image.frombytes(raw_data, (width, height), "ARGB")
        
        plt.close(fig)
        return surface