import requests
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer

class DeepSeekAgent(QThread):
    response_received = pyqtSignal(str)  # 信号：接收到API响应
    def __init__(self, api_key, character_setting):
        super().__init__()
        self.api_key = api_key
        self.history = [{"role": "system", "content": character_setting}]


    
    def chat(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        
        response = requests.post(
            url="https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": "deepseek-chat",
                "messages": self.history,
                "temperature": 0.5,
            }
        )
        ai_reply = response.json()["choices"][0]["message"]["content"]
        self.history.append({"role": "assistant", "content": ai_reply})
        
        self.response_received.emit(ai_reply)
