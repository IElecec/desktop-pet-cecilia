import sys
import requests
import json
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QMovie, QPixmap

class DeepSeekAgent(QThread):
    """后台线程用于执行API调用"""
    response_received = pyqtSignal(str)  # 信号：接收到API响应
    
    def __init__(self, api_key, history, user_input):
        super().__init__()
        self.api_key = api_key
        self.history = history
        self.user_input = user_input
        self.url = "https://api.deepseek.com/v1/chat/completions"
    
    def run(self):
        # 构建包含历史记录的消息
        messages = self.history.copy()
        messages.append({"role": "user", "content": self.user_input})
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 200
        }
        
        response = requests.post(self.url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()  # 检查HTTP错误
        
        data = response.json()
        ai_reply = data["choices"][0]["message"]["content"]
        
        # 发送响应信号
        self.response_received.emit(ai_reply)
            