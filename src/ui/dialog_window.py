import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLineEdit, 
                             QPushButton, QHBoxLayout,QLabel)
from PyQt5.QtCore import Qt,pyqtSignal,QTimer
from PyQt5.QtGui import QFont, QColor, QPainter
import pyautogui
from enum import Enum

class DialogState(Enum):
    SILENT = 0
    TALKING = 1

class AnswerDisplay(QLabel):
    def __init__(self):
        super().__init__()
        
        # 设置窗口属性
        self.setWindowFlags(
            Qt.FramelessWindowHint |  # 无边框
            Qt.WindowStaysOnTopHint | # 始终在最前
            Qt.Tool  # 不显示在任务栏
        )
        self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景
        self.setAttribute(Qt.WA_NoSystemBackground)     # 无系统背景
        
        # 初始化变量
        self.full_text = ""
        self.displayed_text = ""
        self.current_index = 0
        self.typing_speed = 100  # 毫秒
        
        # 设置默认样式
        self.font = QFont("Arial", 10)
        self.color = QColor(255, 255, 255)  # 默认白色
        self.setFont(self.font)
        self.setStyleSheet(f"color: rgba({self.color.red()}, {self.color.green()}, {self.color.blue()}, 255);")
        
        # 设置窗口大小和位置
        screen_width, screen_height = pyautogui.size()
        self.setGeometry(screen_width//2-250, screen_height//2-50, 150, 40)
        
        # 打字效果定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.type_next_character)

        self.setWordWrap(True)
    
    def set_text(self, text):
        """设置要显示的完整文本"""
        self.full_text = text
        self.displayed_text = ""
        self.current_index = 0
        self.timer.start(self.typing_speed)
    
    def type_next_character(self):
        """显示下一个字符"""
        if self.current_index < len(self.full_text):
            self.displayed_text += self.full_text[self.current_index]
            self.setText(self.displayed_text)
            self.adjustSize()  # 调整窗口大小以适应文本
            self.current_index += 1
        else:
            self.timer.stop()
    
    def set_font(self, font_family, size):
        """设置字体和大小"""
        self.font = QFont(font_family, size)
        self.setFont(self.font)
        self.adjustSize()
    
    def set_color(self, r, g, b, a=255):
        """设置文本颜色"""
        self.color = QColor(r, g, b, a)
        self.setStyleSheet(f"color: rgba({r}, {g}, {b}, {a});")
    
    def set_typing_speed(self, speed):
        """设置打字速度(毫秒)"""
        self.typing_speed = speed
        if self.timer.isActive():
            self.timer.setInterval(speed)

class FramelessDialog(QWidget):
    def __init__(self,pet_agent):
        super().__init__()

        self.pet_agent = pet_agent

        self.answer_window = AnswerDisplay()

        self.state = DialogState.SILENT
        
        # 设置无边框窗口
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 设置窗口大小和位置
        # self.setFixedSize(300, 40)
        screen_width, screen_height = pyautogui.size()
        self.setGeometry(screen_width//2-40, screen_height//2+200, 300, 40)
        
        # 创建主布局
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 创建输入框
        self.input_box = QLineEdit()
        self.input_box.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                background: white;
            }
        """)
        
        # 创建发送按钮
        self.send_button = QPushButton("→")
        self.send_button.setFixedWidth(30)  # 设置较小的宽度
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #CFD8A5;
                border: none;
                border-radius: 5px;
                padding: 5px;
                color: #333;
            }
            QPushButton:hover {
                background-color: #B8C28B;
            }
            QPushButton:pressed {
                background-color: #A3AD7A;
            }
        """)
        
        # 将控件添加到布局
        layout.addWidget(self.input_box)
        layout.addWidget(self.send_button)
        
        # 设置布局
        self.setLayout(layout)
        
        # 连接信号
        self.send_button.clicked.connect(self.send_message)
        self.input_box.returnPressed.connect(self.send_message)

        self.pet_agent.position_changed.connect(self.update_position)
        self.pet_agent.state_machine.state_changed.connect(self.update_state)

        self.pet_agent.dialog_agent.answer_changed.connect(self.update_answer)
        
    def send_message(self):
        # 获取输入文本
        text = self.input_box.text()
        
        # 这里不显示发送的信息，只清空输入框
        self.input_box.clear()
        self.hide()
        # 在实际应用中，你可以在这里处理发送逻辑
        self.pet_agent.answer(text)
        self.show()
        
    # def mousePressEvent(self, event):
    #     # 实现窗口拖动
    #     if event.button() == Qt.LeftButton:
    #         self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
    #         event.accept()
            
    # def mouseMoveEvent(self, event):
    #     # 实现窗口拖动
    #     if hasattr(self, 'drag_position') and event.buttons() == Qt.LeftButton:
    #         self.move(event.globalPos() - self.drag_position)
    #         event.accept()

    def update_position(self,new_pos_x,new_pos_y):
        """根据Pet的位置修改window的位置"""
        self.move_to(new_pos_x,new_pos_y)

    def move_to(self,new_pos_x,new_pos_y):
        self.move(new_pos_x-40,new_pos_y+200)
        self.answer_window.move(new_pos_x-250,new_pos_y-50)

    def update_state(self):
        if self.state == DialogState.SILENT:
            self.state = DialogState.TALKING
        else:
            self.state = DialogState.SILENT
            self.do_hide()

    def update_answer(self,message):
        self.answer_window.show()
        self.answer_window.set_text(message)

    def do_hide(self):
        self.hide()
        self.answer_window.hide()

    def do_show(self):
        self.show()
        self.answer_window.show()