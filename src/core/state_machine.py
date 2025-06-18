from enum import Enum
from PyQt5.QtCore import QObject, pyqtSignal

class PetState(Enum):
    IDLE = 0
    WALKING = 1
    SLEEPING = 2
    EATING = 3

class StateMachine(QObject):
    state_changed = pyqtSignal(PetState)  # 状态改变信号
    
    def __init__(self):
        super().__init__()
        self.current_state = PetState.IDLE
        self.previous_state = None
    
    def set_state(self, new_state):
        """设置新状态"""
        if new_state != self.current_state:
            self.previous_state = self.current_state
            self.current_state = new_state
            self.state_changed.emit(new_state)
    
    def execute_current_state(self):
        """执行当前状态的行为"""
        if self.current_state == PetState.WALKING:
            self.walk()
        elif self.current_state == PetState.SLEEPING:
            self.sleep()
        elif self.current_state == PetState.EATING:
            self.eat()
            
    def walk(self):
        """行走行为逻辑"""
        # 实现行走路径和边界检测
        pass
    
    def sleep(self):
        """睡觉行为逻辑"""
        # 恢复能量值
        pass
    
    def eat(self):
        """吃东西行为逻辑"""
        # 播放吃东西动画，然后返回空闲状态
        pass
    
    def play(self):
        """玩耍行为逻辑"""
        # 播放玩耍动画，然后返回空闲状态
        pass