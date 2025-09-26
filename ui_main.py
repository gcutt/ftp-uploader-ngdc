from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,
    QLineEdit, QApplication, QSizePolicy, QProgressBar,
    QListWidget, QListWidgetItem
)
import os

class FTPUploaderUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NGDC FTP Uploader")
        self.resize(500, 300)

        self.layout = QVBoxLayout()

        self.status_label = QLabel("Provide a name for target directory and\nSelect local files to upload")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout.addWidget(self.status_label)

        self.dir_input = QLineEdit()
        self.dir_input.setPlaceholderText("Enter target folder name for remote site (e.g. data_for_ncei)")
        self.dir_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout.addWidget(self.dir_input)

        self.select_button = QPushButton("📁 Select Local Files")
        self.select_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.select_button.clicked.connect(self.select_file)
        self.layout.addWidget(self.select_button)

        self.upload_button = QPushButton("🚀 Upload to NGDC FTP")
        self.upload_button.setEnabled(False)
        self.upload_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.upload_button.clicked.connect(self.upload)
        self.layout.addWidget(self.upload_button)

        self.retry_button = QPushButton("🔄 Retry Failed Uploads")
        self.retry_button.setEnabled(False)
        self.retry_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.retry_button.clicked.connect(self.retry_failed_uploads)
        self.layout.addWidget(self.retry_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout.addWidget(self.progress_bar)

        self.file_list = QListWidget()
        self.file_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.file_list)

        self.layout.addStretch()
        self.setLayout(self.layout)

        self.file_paths = []
        self.total_transferred = 0

    def select_file(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Choose Files")
        if paths:
            self.file_paths = paths
            self.file_list.clear()
            for path in paths:
                item = QListWidgetItem(os.path.basename(path))
                item.setData(Qt.UserRole, path)
                self.file_list.addItem(item)
            self.status_label.setText(f"{len(paths)} file(s) ready to upload")
            self.upload_button.setEnabled(True)
            self.retry_button.setEnabled(False)

    def update_progress(self, filename, file_bytes, total_bytes):
        self.progress_bar.setValue(total_bytes)
        self.status_label.setText(
            f"Uploading {os.path.basename(filename)}: {file_bytes:,} bytes\nTotal: {total_bytes:,} bytes"
        )
        QApplication.processEvents()

    def mark_file_done(self, filename, success):
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            if item.text() == filename:
                color = Qt.green if success else Qt.red
                icon = QIcon("✅") if success else QIcon("❌")
                item.setForeground(color)
                item.setIcon(icon)
                break

        # Check if any failures remain
        has_failures = any(
            self.file_list.item(i).foreground().color() == Qt.red
            for i in range(self.file_list.count())
        )
        self.retry_button.setEnabled(has_failures)

    def upload(self):
        folder_name = self.dir_input.text().strip()
        if not folder_name:
            self.status_label.setText("❌ Please enter a target folder name.")
            return

        if self.file_paths:
            from ftp_client import uploadfiles
            self.total_size = sum(os.path.getsize(p) for p in self.file_paths)
            self.progress_bar.setMaximum(self.total_size)
            self.progress_bar.setValue(0)
            self.progress_bar.setVisible(True)
            self.total_transferred = 0
            self.status_label.setText("Uploading...")

            result = uploadfiles(
                self.file_paths,
                folder_name,
                progress_callback=self.update_progress,
                file_done_callback=self.mark_file_done
            )

            self.status_label.setText(result)
            self.progress_bar.setVisible(False)

    def retry_failed_uploads(self):
        failed_paths = []
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            if item.foreground().color() == Qt.red:
                failed_paths.append(item.data(Qt.UserRole))

        if not failed_paths:
            self.status_label.setText("✅ No failed files to retry.")
            self.retry_button.setEnabled(False)
            return

        folder_name = self.dir_input.text().strip()
        if not folder_name:
            self.status_label.setText("❌ Please enter a target folder name.")
            return

        from ftp_client import uploadfiles
        self.total_size = sum(os.path.getsize(p) for p in failed_paths)
        self.progress_bar.setMaximum(self.total_size)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.total_transferred = 0
        self.status_label.setText("Retrying failed uploads...")

        result = uploadfiles(
            failed_paths,
            folder_name,
            progress_callback=self.update_progress,
            file_done_callback=self.mark_file_done
        )

        self.status_label.setText(result)
        self.progress_bar.setVisible(False)