import sys
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPoint
from PyQt5.QtGui import QFont, QColor, QPainter

class TransparentTextDisplay(QLabel):
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
        self.font = QFont("Arial", 24)
        self.color = QColor(255, 255, 255)  # 默认白色
        self.setFont(self.font)
        self.setStyleSheet(f"color: rgba({self.color.red()}, {self.color.green()}, {self.color.blue()}, 255);")
        
        # 设置窗口大小和位置
        self.resize(800, 100)
        self.move(100, 100)
        
        # 打字效果定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.type_next_character)
    
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 创建透明文本显示
    text_display = TransparentTextDisplay()
    
    # 设置文本内容
    text_display.set_text("这是一个透明背景的逐字显示效果演示。你可以自定义字体、颜色和显示速度。")
    
    # 自定义样式 (可选)
    text_display.set_font("Microsoft YaHei", 30)  # 设置字体和大小
    text_display.set_color(0, 255, 0, 255)      # 设置颜色为绿色
    
    # 显示文本
    text_display.show()
    
    sys.exit(app.exec_())