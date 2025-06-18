import sys
from PyQt5.QtWidgets import QApplication
from src.core import PetAgent
from src.ui import PetWindow,TrayIcon

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # 初始化桌宠代理
    pet_agent = PetAgent()
    print("Pet agent created.")
    # 创建桌宠窗口
    pet_window = PetWindow(pet_agent)
    print("Pet window created.")
    # 创建系统托盘图标
    tray_icon = TrayIcon(app, pet_window)
    print("tray icon created.")
    tray_icon.show()
    print("tray icon showed.")
    
    # 启动桌宠
    pet_agent.start()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()