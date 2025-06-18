import time
import random
from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from .state_machine import PetState, StateMachine

class PetAgent(QObject):
    
    def __init__(self):
        super().__init__()
        self.state_machine = StateMachine()
        self.position = (100, 100)  # 初始位置
        
        # 状态更新定时器
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_state)
        self.update_timer.setInterval(1000)  # 每秒更新一次状态
        
    def start(self):
        """启动桌宠代理"""
        self.update_timer.start()
        self.state_machine.set_state(PetState.IDLE)
        
    def update_state(self):
        """更新桌宠状态"""
        pass
        
    def feed(self):
        """喂食交互"""
        pass
    
    def move_to(self, x, y):
        """移动桌宠到指定位置"""
        self.position = (x, y)