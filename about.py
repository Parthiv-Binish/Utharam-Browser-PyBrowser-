from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton, 
                            QHBoxLayout, QFrame)
from PyQt5.QtGui import QPixmap, QDesktopServices
from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtSvg import QSvgWidget
from resources import AnimationPlayer
from config import GITHUB_URL

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About Utharam Browser")
        self.setFixedSize(500, 500)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel()
        header.setPixmap(QPixmap("logo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Title
        title = QLabel("<h1>Utharam Browser</h1>")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white;")
        layout.addWidget(title)
        
        # Version
        version = QLabel("<b>Version 2.0</b>")
        version.setAlignment(Qt.AlignCenter)
        version.setStyleSheet("color: #9aa0a6;")
        layout.addWidget(version)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("color: #3c4043;")
        layout.addWidget(separator)
        
        # Description
        desc = QLabel("""
        <p>A modern, lightweight browser built with PyQt5</p>
        <p>Developed by Parthiv for teaching GUI and web programming</p>
        <p style="margin-top: 15px;"><b>Features include:</b></p>
        <ul>
            <li>Tab grouping with colors</li>
            <li>Built-in developer tools</li>
            <li>Incognito browsing mode</li>
            <li>Bookmark and history management</li>
            <li>Download manager</li>
            <li>Chrome-like interface</li>
        </ul>
        """)
        desc.setStyleSheet("color: black;")
        desc.setStyleSheet("color: #e8eaed;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # GitHub button
        github_btn = QPushButton("View on GitHub")
        github_btn.setStyleSheet("""
            QPushButton {
                background: #3c4043;
                color: white;
                border-radius: 4px;
                padding: 8px;
            }
            QPushButton:hover {
                background: #5f6368;
            }
        """)
        github_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(GITHUB_URL)))
        layout.addWidget(github_btn)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet("""
            QPushButton {
                background: #1a73e8;
                color: white;
                border-radius: 4px;
                padding: 8px;
            }
            QPushButton:hover {
                background: #2b7de9;
            }
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        
        # Add animation
        self.animation = AnimationPlayer(self)
        self.animation.load_animation("animations/success")
        self.animation.move(400, 400)
        self.animation.show()