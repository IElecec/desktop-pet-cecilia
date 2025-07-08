import time
import random
from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from .state_machine import PetState, StateMachine
from .dialog_agent import DialogAgent
import pyautogui

class PetAgent(QObject):
    position_changed = pyqtSignal(int,int)  # 状态改变信号
    def __init__(self):
        super().__init__()
        self.state_machine = StateMachine()
        self.dialog_agent = DialogAgent()

        self.screen_width, self.screen_height = pyautogui.size()
        self.position_x = self.screen_width//2
        self.position_y = self.screen_height//2

        # 状态更新定时器
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_state)
        self.update_timer.setInterval(100)  # 每秒更新一次状态
        
    def start(self):
        """启动桌宠代理"""
        self.update_timer.start()
        self.state_machine.set_state(PetState.IDLE)
        
    def update_state(self):
        """更新桌宠状态"""
        if self.state_machine.current_state == PetState.WALKING:
            if self.position_x + 100 < self.screen_width:
                self.position_x +=5
                self.position_changed.emit(self.position_x,self.position_y)
        
    # def feed(self):
    #     """喂食交互"""
    #     pass

    def sleep(self):
        self.state_machine.set_state(PetState.FALL_ASLEEP)

    def idle(self):
        self.state_machine.set_state(PetState.IDLE)

    def walk(self):
        self.state_machine.set_state(PetState.WALKING)

    def talk(self):
        self.state_machine.set_state(PetState.TALKING)
    
    def move_to(self, x, y):
        """移动桌宠到指定位置"""
        self.position_x = x
        self.position_y = y

    def answer(self,message):
        self.dialog_agent.answer(message)
