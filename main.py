"""
"""

# from PySide6.QtWidgets import QApplication, QMainWindow
# from ui_main import Ui_MainWindow  # assuming this is your generated UI class
# import sys
from PySide6.QtWidgets import QApplication
from ui_main import FTPUploaderUI
import sys


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)  # this attaches the UI to the main window

#         print(dir(self.ui))    # Inspect available widgets


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FTPUploaderUI()
    window.show()
    sys.exit(app.exec())