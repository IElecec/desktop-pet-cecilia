from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt, QPoint, QTimer, pyqtSignal
from PyQt5.QtGui import QMovie, QPixmap, QPainter, QColor, QMouseEvent
from src.core import PetState
from src.utils import load_animation

class PetWindow(QWidget):
    position_changed = pyqtSignal(int, int)  # 位置改变信号
    
    def __init__(self, pet_agent):
        super().__init__()
        self.pet_agent = pet_agent
        self.drag_position = QPoint()
        
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        # 设置窗口属性
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.SubWindow
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        
        # 设置初始位置和大小
        self.setGeometry(100, 100, 200, 200)
        
        # 动画标签
        self.animation_label = QLabel(self)
        self.animation_label.setAlignment(Qt.AlignCenter)
        self.animation_label.setGeometry(0, 0, 200, 200)
        
        # 加载初始动画
        self.update_animation(PetState.IDLE)
        
        # 更新动画的定时器
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation_frame)
        self.animation_timer.start(20)  # 每100ms更新一帧
        
    def setup_connections(self):
        # 连接状态改变信号
        self.pet_agent.state_machine.state_changed.connect(self.update_animation)
        
    def update_animation(self, state):
        """根据状态更新动画"""
        animation_frames = load_animation(state)
        if animation_frames:
            self.current_animation = animation_frames
            self.current_frame_index = 0
            self.update_animation_frame()
    
    def update_animation_frame(self):
        """更新当前动画帧"""
        if hasattr(self, 'current_animation') and self.current_animation:
            frame_path = self.current_animation[self.current_frame_index]
            pixmap = QPixmap(frame_path)
            self.animation_label.setPixmap(pixmap)
            
            # 更新到下一帧
            self.current_frame_index = (self.current_frame_index + 1) % len(self.current_animation)
    
    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件，开始拖拽"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """鼠标移动事件，拖拽窗口"""
        if event.buttons() == Qt.LeftButton:
            new_pos = event.globalPos() - self.drag_position
            self.move(new_pos)
            self.position_changed.emit(new_pos.x(), new_pos.y())
            event.accept()
    
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """双击事件，触发互动"""
        pass