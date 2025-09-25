"""
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,
    QLineEdit, QApplication, QSizePolicy
)

class FTPUploaderUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NGDC FTP Uploader")
        self.resize(500, 250)  # Initial size, now resizable

        self.layout = QVBoxLayout()

        # Status label
        self.status_label = QLabel("Provide a name for target directory and\nSelect local files to upload")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout.addWidget(self.status_label)

        # Directory input
        self.dir_input = QLineEdit()
        self.dir_input.setPlaceholderText("Enter target folder name for remote site (e.g. data_for_ncei)")
        self.dir_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout.addWidget(self.dir_input)

        # Select files button
        self.select_button = QPushButton("📁 Select Local Files")
        self.select_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.select_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.select_button)

        # Upload button
        self.upload_button = QPushButton("🚀 Upload to NGDC FTP")
        self.upload_button.setEnabled(False)
        self.upload_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.upload_button.clicked.connect(self.upload)
        self.layout.addWidget(self.upload_button)

        # Add stretch to improve vertical spacing
        self.layout.addStretch()

        self.setLayout(self.layout)

        # File paths container
        self.file_paths = []

    def select_file(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Choose Files")
        if paths:
            self.file_paths = paths
            self.status_label.setText(f"{len(paths)} file(s) ready to upload")
            self.upload_button.setEnabled(True)

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

if __name__ == "__main__":
    app = QApplication([])
    window = FTPUploaderUI()
    window.show()
    app.exec()



# from PySide6.QtCore import Qt

# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QApplication
# )
# # ... rest unchanged ...

# class FTPUploaderUI(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("NGDC FTP Uploader")
#         self.setFixedSize(500, 250)

#         self.layout = QVBoxLayout()

#         self.status_label = QLabel(f"Provide a name fortarget directory and\nSelect local files to upload")
#         self.status_label.setAlignment(Qt.AlignCenter)

#         self.dir_input = QLineEdit()
#         self.dir_input.setPlaceholderText("Enter target folder name for remote site (e.g. data_for_ncei)")

#         self.select_button = QPushButton("📁 Select ocal Files")
#         self.upload_button = QPushButton("🚀 Upload to NGDC FTP")
#         self.upload_button.setEnabled(False)

#         self.select_button.clicked.connect(self.select_file)
#         self.upload_button.clicked.connect(self.upload)

#         self.layout.addWidget(self.status_label)
#         self.layout.addWidget(self.dir_input)
#         self.layout.addWidget(self.select_button)
#         self.layout.addWidget(self.upload_button)
#         self.setLayout(self.layout)

#         # self.file_path = None
#         self.file_paths = []

#     def select_file(self):
#         paths, _ = QFileDialog.getOpenFileNames(self, "Choose Files")
#         if paths:
#             self.file_paths = paths
#             self.status_label.setText(f"{len(paths)} file(s) ready to upload")
#             self.upload_button.setEnabled(True)

#     def upload(self):
#         folder_name = self.dir_input.text().strip()
#         if not folder_name:
#             self.status_label.setText("❌ Please enter a target folder name.")
#             return

#         if self.file_paths:
#             self.status_label.setText("Uploading...")
#             from ftp_client import uploadfiles
#             result = uploadfiles(self.file_paths, folder_name)
#             self.status_label.setText(result)