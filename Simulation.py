import pygame as py
import pygame_gui as pyg
import sys, time
from PlayerInfoUIObserver import PlayerInfoUIObserver
from MarketInfoUIObserver import MarketInfoUIObserver
from Player import Player
from Market import Market
from NormalState import NormalState
from EventFactory import EventFactory
import random


class Simulation():
    def __init__(self, window_height: int, window_width: int):
        self.running = True
        self.window_height = window_height
        self.window_width = window_width
        py.init()
        self.screen = py.display.set_mode((self.window_width, self.window_height))  
        self.manager = pyg.UIManager((self.window_width, self.window_height))
        
        self.eventFactory = EventFactory()
        
        py.display.set_caption('SaveTheButter')
        
        self.market = Market.getInstance()
        self.market.attach(MarketInfoUIObserver(self.manager))
        self.market.state = NormalState()
        
        self.clock = py.Clock()        
        self.paused = False
        self.start_time = time.time()
        
        week_label_rect = py.Rect((0, 10), (150, 20))
        self.week_label = pyg.elements.UILabel(week_label_rect, "Tydzien: 0", manager=self.manager, anchors={'centerx': 'centerx', 'top': 'top'})
        self.current_week = 0
        
        self.player = Player()
        self.player.attach(PlayerInfoUIObserver(self.manager))
        
        buy_slider_rect = py.Rect((30, 550), (500, 30))
        self.buy_slider = pyg.elements.UIHorizontalSlider(buy_slider_rect, 0, (0, self.player.warehouse.capacity - self.player.butter), self.manager)
        self.buy_slider.enable_arrow_buttons = False
        self.buy_slider.rebuild()
        
        buy_slider_label_rect = py.Rect((560, 550), (100, 30))
        self.buy_slider_label = pyg.elements.UILabel(buy_slider_label_rect, f"{self.buy_slider.get_current_value()} kg", manager=self.manager)
        
        buy_value_label_rect = py.Rect((690,550),(100,30))
        self.buy_value_label = pyg.elements.UILabel(buy_value_label_rect, f"{(self.buy_slider.get_current_value() * self.market.price):.2f} PLN", manager=self.manager)
        
        buy_btn_rect = py.Rect((830, 550), (100, 30))
        self.buy_btn = pyg.elements.UIButton(buy_btn_rect, "Kup", manager=self.manager)
        
        sell_slider_rect = py.Rect((30, 620), (500, 30))
        self.sell_slider = pyg.elements.UIHorizontalSlider(sell_slider_rect, 0, (0, self.player.butter), self.manager)
        self.sell_slider.enable_arrow_buttons = False
        self.sell_slider.rebuild()
        
        sell_slider_label_rect = py.Rect((560, 620), (100, 30))
        self.sell_slider_label = pyg.elements.UILabel(sell_slider_label_rect, f"{self.sell_slider.get_current_value()} kg", manager=self.manager)
        
        sell_value_label_rect = py.Rect((690,620),(100,30))
        self.sell_value_label = pyg.elements.UILabel(sell_value_label_rect, f"{(self.sell_slider.get_current_value() * self.market.price):.2f} PLN", manager=self.manager)
        
        sell_btn_rect = py.Rect((830, 620), (100, 30))
        self.sell_btn = pyg.elements.UIButton(sell_btn_rect, "Sprzedaj", manager=self.manager)
        
        upgrade_btn_rect = py.Rect((0, 50), (200, 30))
        self.upgrade_btn= pyg.elements.UIButton(upgrade_btn_rect,
                                                "Ulepsz magazyn",
                                                manager=self.manager,
                                                anchors={'centerx': 'centerx', 'top': 'top'},
                                                tool_tip_text=f"Magazyn moze byc ulepszony maksymalnie 4 razy.\nAktualny poziom to 1.\nCena wynajmu wynosi {self.player.warehouse.rent_cost} PLN rocznie.")
        
        self.current_dialog = None
    
    def showEventDialog(self, message):
        dialog_rect = py.Rect((self.window_width // 4, self.window_height // 4),  
                              (self.window_width // 2, self.window_height // 2))  
        dialog = pyg.elements.UIWindow(dialog_rect,  
                                        self.manager)  
        
        
        message = message + "\n<i>Nacisnij spacje, aby wznowic symulacje.</i>"
        
        textbox = pyg.elements.UITextBox(relative_rect=py.Rect((0, -30), (450, 500)),  
                                            html_text=message,  
                                            manager=self.manager,
                                            anchors={'center': 'center'}, 
                                            wrap_to_height=True, 
                                            container=dialog)   
        self.paused = True
        self.switchInteractibility()
        dialog.enable_close_button = False
        dialog.enable_title_bar = False
        dialog.rebuild()
        return dialog
    
    def switchInteractibility(self):
        if self.paused:
            self.buy_btn.disable()
            self.sell_btn.disable()
            self.buy_slider.disable()
            self.sell_slider.disable()
            self.upgrade_btn.disable()
        else:
            self.buy_btn.enable()
            self.sell_btn.enable()
            self.buy_slider.enable()
            self.sell_slider.enable()
            if self.player.warehouse.level != 4:
                self.upgrade_btn.enable()
    
    def run(self):
        trigger_update = 0
        while self.running:
            delta_time = self.clock.tick(60)
            
            for event in py.event.get():
                if event.type == py.QUIT:
                    self.running = False
                elif event.type == py.KEYDOWN:
                    if event.key == py.K_SPACE:
                        self.paused = not self.paused
                        self.switchInteractibility()
                        if self.current_dialog:
                            self.current_dialog.kill()
                elif event.type == pyg.UI_BUTTON_PRESSED:
                    if event.ui_element == self.buy_btn:
                        self.player.buyButter(self.buy_slider.get_current_value())
                        self.buy_slider.set_current_value(0)
                    elif event.ui_element == self.sell_btn:
                        self.player.sellButter(self.sell_slider.get_current_value())
                        self.sell_slider.set_current_value(0)
                    elif event.ui_element == self.upgrade_btn:
                        if not self.player.upgradeWarehouse():
                            self.upgrade_btn.disable()
                        else:
                            level = self.player.warehouse.level
                            rent = self.player.warehouse.rent_cost
                            self.upgrade_btn.set_tooltip(f"Magazyn moze byc ulepszony maksymalnie 4 razy.\nAktualny poziom to {level}.\nCena wynajmu wynosi {rent} PLN rocznie.")
                    if event.ui_object_id != "horizontal_slider.#sliding_button":
                        warehouse_limit = self.player.warehouse.capacity - self.player.butter
                        self.buy_slider.value_range = (0, warehouse_limit)
                        self.sell_slider.value_range = (0, self.player.butter)
                        self.buy_slider.rebuild()
                        self.sell_slider.rebuild()
                        self.buy_slider_label.set_text("0 kg")
                        self.sell_slider_label.set_text("0 kg")
                elif event.type == pyg.UI_HORIZONTAL_SLIDER_MOVED:
                    approx_value = round(event.value/5) * 5
                    if event.ui_element == self.buy_slider:
                        self.buy_slider.set_current_value(approx_value)
                        self.buy_slider_label.set_text(f"{approx_value} kg")
                        self.buy_value_label.set_text(f"{(approx_value * self.market.price):.2f} PLN")
                        self.sell_value_label.set_text("0.00 PLN")
                        self.sell_slider.set_current_value(0)
                        self.sell_slider_label.set_text("0 kg")    
                    elif event.ui_element == self.sell_slider:
                        self.sell_slider.set_current_value(approx_value)
                        self.sell_slider_label.set_text(f"{approx_value} kg")    
                        self.sell_value_label.set_text(f"{(approx_value * self.market.price):.2f} PLN")
                        self.buy_value_label.set_text("0.00 PLN")
                        self.buy_slider.set_current_value(0)
                        self.buy_slider_label.set_text("0 kg")    
                self.manager.process_events(event)
            
            self.screen.fill((0, 0, 0))
            self.week_label.set_text(f"Tydzien: {self.current_week}")
            
            if not self.paused:
                if hasattr(self, 'pause_time'):
                    paused_duartion = time.time() - self.pause_time
                    self.start_time += paused_duartion
                    del self.pause_time
                time_elapsed = time.time() - self.start_time
                if time_elapsed > trigger_update: 
                    
                    if self.market.state.__class__.__name__ == "NormalState":
                        chance = random.random()
                        if chance < 0.1:
                            event = self.eventFactory.getRandomEvent()
                            event.happen()
                            self.current_dialog = self.showEventDialog(event.eventMessage())
                        
                    self.market.update(self.current_week)
                    
                    self.current_week += 1
                    trigger_update += 2
                    self.sell_value_label.set_text(f"{(self.sell_slider.get_current_value() * self.market.price):.2f} PLN")
                    self.buy_value_label.set_text(f"{(self.buy_slider.get_current_value() * self.market.price):.2f} PLN")
                    
                    if self.current_week % 52 == 0:
                        if not self.player.payRent():
                            self.running = False
                        self.market.base_price *= random.uniform(1.01, 1.08)
            else:
                if not hasattr(self, 'pause_time'):
                    self.pause_time = time.time()
                
            plot_surface = self.market.createChart()
                
            self.screen.blit(plot_surface, (30, 120))
                                
            self.manager.update(delta_time)
            
            self.manager.draw_ui(self.screen)
            
            py.display.flip()

        py.quit()
        sys.exit(0)