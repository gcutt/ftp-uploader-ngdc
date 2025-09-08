"""
"""
from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QApplication
)
# ... rest unchanged ...

class FTPUploaderUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NGDC FTP Uploader")
        self.setFixedSize(400, 250)

        self.layout = QVBoxLayout()

        self.status_label = QLabel(f"Name target directory and\nSelect files to upload")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.dir_input = QLineEdit()
        self.dir_input.setPlaceholderText("Enter target folder name (e.g. data_for_ncei)")

        self.select_button = QPushButton("📁 Select Files")
        self.upload_button = QPushButton("🚀 Upload to NGDC FTP")
        self.upload_button.setEnabled(False)

        self.select_button.clicked.connect(self.select_file)
        self.upload_button.clicked.connect(self.upload)

        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.dir_input)
        self.layout.addWidget(self.select_button)
        self.layout.addWidget(self.upload_button)
        self.setLayout(self.layout)

        # self.file_path = None
        self.file_paths = []

    # def select_file(self):
    #     path, _ = QFileDialog.getOpenFileName(self, "Choose File")
    #     if path:
    #         self.file_path = path
    #         self.status_label.setText(f"Ready to upload: {path}")
    #         self.upload_button.setEnabled(True)

    def select_file(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Choose Files")
        if paths:
            self.file_paths = paths
            self.status_label.setText(f"{len(paths)} file(s) ready to upload")
            self.upload_button.setEnabled(True)
            
    # def upload(self):
    #     folder_name = self.dir_input.text().strip()
    #     if not folder_name:
    #         self.status_label.setText("❌ Please enter a target folder name.")
    #         return

    #     if self.file_path:
    #         self.status_label.setText("Uploading...")
    #         from ftp_client import uploadfile
    #         result = uploadfile(self.file_path, folder_name)
    #         self.status_label.setText(result)

    def upload(self):
        folder_name = self.dir_input.text().strip()
        if not folder_name:
            self.status_label.setText("❌ Please enter a target folder name.")
            return

        if self.file_paths:
            self.status_label.setText("Uploading...")
            from ftp_client import uploadfiles
            result = uploadfiles(self.file_paths, folder_name)
            self.status_label.setText(result)