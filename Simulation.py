import pygame as py
import pygame_gui as pyg
import sys, time
from PlayerInfoUIObserver import PlayerInfoUIObserver
from MarketInfoUIObserver import MarketInfoUIObserver
from Market import Market
from NormalState import NormalState
import random


class Simulation:
    def __init__(self, window_height: int, window_width: int):
        self.running = True
        self.window_height = window_height
        self.window_width = window_width
        py.init()
        self.screen = py.display.set_mode((self.window_width, self.window_height))  
        self.manager = pyg.UIManager((self.window_width, self.window_height))
        py.display.set_caption('SaveTheButter')
        obs = PlayerInfoUIObserver(self.manager)
        self.market = Market.getInstance()
        self.market.attach(MarketInfoUIObserver(self.manager))
        self.market.setState(NormalState())
        self.clock = py.Clock()        
        self.start_time = time.time()
        week_label_rect = py.Rect((0, 10), (150, 20))
        self.week_label = pyg.elements.UILabel(week_label_rect, "Tydzien: 0", manager=self.manager, anchors={'centerx': 'centerx', 'top': 'top'})
        self.current_week = 0
    
    def run(self):
        trigger_update = 0
        while self.running:
            delta_time = self.clock.tick(60)
            time_elapsed = time.time() - self.start_time
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.running = False
                elif event.type == pyg.UI_BUTTON_PRESSED:
                    pass
                self.manager.process_events(event)
            
            self.screen.fill((0, 0, 0))
            self.week_label.set_text(f"Tydzien: {self.current_week}")
            
            if time_elapsed > trigger_update: 
                self.market.update()
                self.current_week += 1
                trigger_update += 2
                if self.current_week % 52 == 0:
                    self.market.basePrice *= random.uniform(1.01, 1.08)
                    
            self.manager.update(delta_time)
            
            self.manager.draw_ui(self.screen)
            
            py.display.flip()

        py.quit()
        sys.exit(0)