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
        self.init_menu()
        
        
        
        # 点击托盘图标事件
        # self.activated.connect(self.on_tray_activated)

    def init_menu(self):
        self.menu = QMenu()

        # 添加分隔线
        self.menu.addSeparator() 

        # 显示/隐藏宠物
        self.toggle_action = QAction("显示/隐藏", self)
        self.toggle_action.triggered.connect(self.toggle_pet)
        self.menu.addAction(self.toggle_action)
        
        # 退出
        self.quit_action = QAction("退出", self)
        self.quit_action.triggered.connect(self.quit_app)
        self.menu.addAction(self.quit_action)

        self.setContextMenu(self.menu)

    def toggle_pet(self):
        """切换桌宠显示状态"""
        self.pet_window.toggle_pet()
    
    def quit_app(self):
        """退出应用程序"""
        self.app.quit()
    
    def on_tray_activated(self, reason):
        """托盘图标被激活时的处理"""
        if reason == QSystemTrayIcon.Trigger:
            self.toggle_pet()