from pathlib import Path
from datetime import datetime
import os
from PyQt5.QtCore import QObject, QTimer, pyqtSignal
import json
from .ds_api import DeepSeekAgent

def load_key_from_json(file_path, key_name='secret_key'):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data.get(key_name)

class DialogAgent(QObject):
    answer_changed = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setup_logger()
        self.setup_llm_api()

    def setup_logger(self):
        
        self.log_dir = Path("logs/")
        today = datetime.now().strftime("%Y-%m-%d")
        self.log_file = os.path.join(self.log_dir, f"{today}.log")
        
        # 写入初始信息
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"\n\n=== 新会话开始于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")

    def setup_llm_api(self):
        API_KEY = load_key_from_json('secret.json')
    
        self.character = DeepSeekAgent(
            api_key=API_KEY,
            character_setting="你是一位名叫塞西莉亚的小修女，居住在一座小镇上，既慵懒又可爱，平时最喜欢做的事情是吃甜品，有着灰绿色的漂亮长发。"
        )

        self.character.response_received.connect(self.handle_answer)
    
    def answer(self,message):
        print(message)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"User:{message}\n")
        self.character.chat(message)

    def handle_answer(self,answer):
        print(answer)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"Cecilia:{answer}\n\n")
        self.answer_changed.emit(answer)