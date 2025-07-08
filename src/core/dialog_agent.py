from pathlib import Path
from datetime import datetime
import os
from PyQt5.QtCore import QObject, QTimer, pyqtSignal

class DialogAgent(QObject):
    answer_changed = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setup_logger()
        # 创建日志文件路径

    def setup_logger(self):
        
        self.log_dir = Path("logs/")
        today = datetime.now().strftime("%Y-%m-%d")
        self.log_file = os.path.join(self.log_dir, f"{today}.log")
        
        # 写入初始信息
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"\n\n=== 新会话开始于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")
    
    def answer(self,message):
        print(message)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"User:{message}\n")
            f.write(f"Cecilia:QAQ\n\n")
        self.answer_changed.emit("QAQ")