from PyQt5.QtWidgets import QWidget, QLabel, QMenu, QAction
from PyQt5.QtCore import Qt, QPoint, QTimer, pyqtSignal
from PyQt5.QtGui import QMovie, QPixmap, QPainter, QColor, QMouseEvent
from src.core import PetState
from src.utils import load_animation
import pyautogui

class PetWindow(QWidget):
    position_changed = pyqtSignal(int, int)  # 位置改变信号
    
    def __init__(self, pet_agent):
        super().__init__()
        self.pet_agent = pet_agent
        self.drag_position = QPoint()
        
        self.init_menu()

        self.init_ui()
        
        self.setup_connections()

    def init_menu(self):
        self.menu = QMenu()
        
        # 空闲
        self.idle_action = QAction("空闲", self)
        self.idle_action.triggered.connect(self.idle_pet)
        self.menu.addAction(self.idle_action)
        
        # # 喂食
        # self.feed_action = QAction("喂食", self)
        # self.feed_action.triggered.connect(self.feed_pet)
        # self.menu.addAction(self.feed_action)

        # 睡觉
        self.sleep_action = QAction("睡觉", self)
        self.sleep_action.triggered.connect(self.sleep_pet)
        self.menu.addAction(self.sleep_action)

        # 散步
        self.walk_action = QAction("散步", self)
        self.walk_action.triggered.connect(self.walk_pet)
        self.menu.addAction(self.walk_action)

        # 添加分隔线
        self.menu.addSeparator() 

        # 隐藏宠物
        self.toggle_action = QAction("隐藏", self)
        self.toggle_action.triggered.connect(self.toggle_pet)
        self.menu.addAction(self.toggle_action)

        # # 设置上下文菜单策略
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, pos):
        # 创建菜单对象
        context_menu = self.menu

        # 显示菜单
        context_menu.exec_(self.mapToGlobal(pos))
        
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
        screen_width, screen_height = pyautogui.size()
        self.setGeometry(screen_width//2, screen_height//2, 200, 200)
        
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
        self.pet_agent.position_changed.connect(self.update_position)
        
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
            if self.pet_agent.state_machine.is_transient() and self.current_frame_index + 1 == len(self.current_animation):
                self.pet_agent.state_machine.end_transient()
            else:
                self.current_frame_index = (self.current_frame_index + 1) % len(self.current_animation)

    def update_position(self,new_pos_x,new_pos_y):
        """根据Pet的位置修改window的位置"""
        self.move(new_pos_x,new_pos_y)
        self.position_changed.emit(new_pos_x, new_pos_y)

    
    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下事件，开始拖拽"""
        if event.button() == Qt.LeftButton:
            self.pet_agent.idle()
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """鼠标移动事件，拖拽窗口"""
        if event.buttons() == Qt.LeftButton:
            new_pos = event.globalPos() - self.drag_position
            self.move(new_pos)
            self.pet_agent.move_to(new_pos.x(), new_pos.y())
            self.position_changed.emit(new_pos.x(), new_pos.y())
            event.accept()
    
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """双击事件，触发互动"""
        pass

    def toggle_pet(self):
        """切换桌宠显示状态"""
        if self.isVisible():
            print("hide")
            self.hide()
        else:
            print("show")
            self.show()
    
    def feed_pet(self):
        """喂食桌宠"""
        self.pet_agent.feed()

    def sleep_pet(self):
        """桌宠睡觉"""
        self.pet_agent.sleep()

    def idle_pet(self):
        """闲置桌宠"""
        self.pet_agent.idle()

    def walk_pet(self):
        """桌宠走路"""
        self.pet_agent.walk()
    