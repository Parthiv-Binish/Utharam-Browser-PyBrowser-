from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QToolBar, 
                            QAction, QMessageBox, QProgressBar, QFileDialog)
from PyQt5.QtWebEngineWidgets import (QWebEngineView, QWebEngineProfile, 
                                     QWebEnginePage, QWebEngineDownloadItem,
                                     QWebEngineSettings)
from PyQt5.QtCore import pyqtSignal, QUrl, Qt, QTimer
from PyQt5.QtGui import QIcon
from resources import AnimationPlayer
from icons import Icons
import re
import os
import urllib.parse
import uuid
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BrowserTab(QWidget):
    urlChanged = pyqtSignal(str)
    titleChanged = pyqtSignal(str)

    def __init__(self, parent=None, incognito=False):
        super().__init__(parent)
        self.tab_id = str(uuid.uuid4())  # Generate unique ID for the tab
        self.incognito = incognito
        self.profile = QWebEngineProfile.defaultProfile() if not incognito else QWebEngineProfile()
        self.page = QWebEnginePage(self.profile, self)
        self.browser = QWebEngineView(self)
        self.browser.setPage(self.page)
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        # Create toolbar
        self.create_toolbar()

        # Add browser view
        self.layout.addWidget(self.browser)

        # Loading animation
        self.loading_animation = AnimationPlayer(self)
        self.loading_animation.hide()
        self.layout.addWidget(self.loading_animation, alignment=Qt.AlignCenter)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(3)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: transparent;
                border: none;
            }
            QProgressBar::chunk {
                background: #1a73e8;
            }
        """)
        self.layout.addWidget(self.progress_bar)

        # Connect signals
        self.browser.urlChanged.connect(self.update_url)
        self.browser.titleChanged.connect(self.update_title)
        self.browser.loadStarted.connect(self.show_loading)
        self.browser.loadProgress.connect(self.update_progress)
        self.browser.loadFinished.connect(self.hide_loading)
        self.profile.downloadRequested.connect(self.handle_download)

        # Enable dev tools
        self.page.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        self.page.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        self.page.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)

        # Set initial URL
        self.browser.setUrl(QUrl("https://www.google.com"))

    def create_toolbar(self):
        self.toolbar = QToolBar()
        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet("""
            QToolBar {
                background: #2d2e30;
                border: none;
                padding: 2px;
            }
        """)

        # Back button
        self.back_btn = QAction(Icons.back(), "Back", self)
        self.back_btn.setToolTip("Back")
        self.back_btn.triggered.connect(self.browser.back)
        self.toolbar.addAction(self.back_btn)

        # Forward button
        self.forward_btn = QAction(Icons.forward(), "Forward", self)
        self.forward_btn.setToolTip("Forward")
        self.forward_btn.triggered.connect(self.browser.forward)
        self.toolbar.addAction(self.forward_btn)

        # Reload button
        self.reload_btn = QAction(Icons.reload(), "Reload", self)
        self.reload_btn.setToolTip("Reload")
        self.reload_btn.triggered.connect(self.browser.reload)
        self.toolbar.addAction(self.reload_btn)

        # Stop button
        self.stop_btn = QAction(Icons.stop(), "Stop", self)
        self.stop_btn.setToolTip("Stop")
        self.stop_btn.triggered.connect(self.browser.stop)
        self.toolbar.addAction(self.stop_btn)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search Google or type URL")
        self.url_bar.setStyleSheet("""
            QLineEdit {
                background: #3c4043;
                border: 1px solid #5f6368;
                border-radius: 15px;
                padding: 5px 15px;
                color: white;
                selection-background-color: #8ab4f8;
            }
        """)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)

        # Add toolbar to layout
        self.layout.addWidget(self.toolbar)

    def navigate_to_url(self):
        text = self.url_bar.text().strip()
        if not text:
            return

        # Stricter URL validation
        url_pattern = re.compile(
            r'^(https?://)?'
            r'(([A-Za-z0-9-]+\.)+[A-Za-z]{2,6}|localhost)'
            r'(:[0-9]{1,5})?(/.*)?$'
        )
        
        if url_pattern.match(text):
            url = text if text.startswith(("http://", "https://")) else "https://" + text
        else:
            # Sanitize search query
            safe_query = urllib.parse.quote(text)
            url = f"https://www.google.com/search?q={safe_query}"
        
        try:
            self.browser.setUrl(QUrl(url))
        except Exception as e:
            QMessageBox.warning(self, "Invalid URL", f"Failed to navigate to {url}: {str(e)}")

    def update_url(self, url):
        self.url_bar.setText(url.toString())
        self.urlChanged.emit(url.toString())

    def update_title(self, title):
        self.titleChanged.emit(title)
        self.urlChanged.emit(title)

    def show_loading(self):
        self.browser.hide()
        self.loading_animation.load_animation("animations/loading")
        self.loading_animation.show()
        self.progress_bar.setValue(0)

    def hide_loading(self):
        self.loading_animation.hide()
        self.browser.show()
        self.progress_bar.setValue(100)
        QTimer.singleShot(500, lambda: self.progress_bar.setValue(0))

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def handle_download(self, download: QWebEngineDownloadItem):
        if self.incognito:
            QMessageBox.warning(self, "Incognito Mode", "Downloads are not supported in incognito mode.")
            return
        
        # Ask for download location
        default_path = os.path.join(os.path.expanduser("~"), "Downloads", download.suggestedFileName())
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", default_path)
        
        if file_path:
            download.setPath(file_path)
            download.accept()
            
            # Show download progress
            download.finished.connect(lambda: self.notify_download_complete(download.suggestedFileName()))
            download.downloadProgress.connect(self.show_download_progress)
        else:
            download.cancel()

    def notify_download_complete(self, file_name):
        QMessageBox.information(self, "Download Complete", f"Downloaded: {file_name}")

    def show_download_progress(self, bytes_received, bytes_total):
        if bytes_total > 0:
            progress = (bytes_received / bytes_total) * 100
            self.url_bar.setText(f"Downloading... {progress:.1f}%")

    def toggle_dev_tools(self):
        if hasattr(self, 'dev_tools_window') and self.dev_tools_window:
            logging.info("Closing DevTools window")
            self.page.setDevToolsPage(None)
            self.dev_tools_window.setPage(None)
            self.dev_tools_window.close()
            self.dev_tools_window.deleteLater()
            self.dev_tools_window = None
            return
        
        logging.info("Opening DevTools window")
        dev_tools_page = QWebEnginePage(self.profile, self)
        self.page.setDevToolsPage(dev_tools_page)
        
        self.dev_tools_window = QWebEngineView()
        self.dev_tools_window.setPage(dev_tools_page)
        self.dev_tools_window.setWindowTitle("Developer Tools")
        self.dev_tools_window.setGeometry(100, 100, 800, 600)
        self.dev_tools_window.show()

    def deleteLater(self):
        logging.info(f"Deleting tab {self.tab_id}")
        try:
            self.browser.urlChanged.disconnect()
            self.browser.titleChanged.disconnect()
            self.browser.loadStarted.disconnect()
            self.browser.loadProgress.disconnect()
            self.browser.loadFinished.disconnect()
            self.profile.downloadRequested.disconnect()
        except TypeError:
            pass  # Signals may already be disconnected
        
        self.loading_animation.deleteLater()
        
        self.browser.setPage(None)
        self.page.deleteLater()
        self.browser.deleteLater()
        
        super().deleteLater()