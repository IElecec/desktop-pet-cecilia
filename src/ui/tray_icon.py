from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

class TrayIcon(QSystemTrayIcon):
    def __init__(self, app, pet_window, parent=None):
        super().__init__(parent)
        self.app = app
        self.pet_window = pet_window
        
        # 设置图标
        self.setIcon(QIcon("assets/icons/cecilia.ico"))
        
        # 创建菜单
        self.menu = QMenu()
        
        # 显示/隐藏宠物
        self.toggle_action = QAction("显示/隐藏桌宠", self)
        self.toggle_action.triggered.connect(self.toggle_pet)
        self.menu.addAction(self.toggle_action)
        
        # 喂食
        self.feed_action = QAction("喂食", self)
        self.feed_action.triggered.connect(self.feed_pet)
        self.menu.addAction(self.feed_action)
        
        # 退出
        self.quit_action = QAction("退出", self)
        self.quit_action.triggered.connect(self.quit_app)
        self.menu.addAction(self.quit_action)
        
        self.setContextMenu(self.menu)
        
        # 点击托盘图标事件
        self.activated.connect(self.on_tray_activated)
    
    def toggle_pet(self):
        """切换桌宠显示状态"""
        if self.pet_window.isVisible():
            print("hide")
            self.pet_window.hide()
        else:
            print("show")
            self.pet_window.show()
    
    def feed_pet(self):
        """喂食桌宠"""
        self.pet_window.pet_agent.feed()
    
    def quit_app(self):
        """退出应用程序"""
        self.app.quit()
    
    def on_tray_activated(self, reason):
        """托盘图标被激活时的处理"""
        if reason == QSystemTrayIcon.Trigger:
            self.toggle_pet()