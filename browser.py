from PyQt5.QtWidgets import (QMainWindow, QToolBar, QAction, QTabWidget, QMenu, 
                            QInputDialog, QColorDialog, QTabBar, QLabel, 
                            QHBoxLayout, QWidget, QSizePolicy, QLineEdit, QMessageBox)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QUrl, QSize
from tab import BrowserTab
from about import AboutDialog
from settings import SettingsDialog
from icons import Icons
from resources import AnimationPlayer
import sqlite3
import os
import json
import uuid
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Utharam Browser")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)

        # Initialize database
        self.init_database()

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.setCentralWidget(self.tabs)

        self.tab_groups = {}
        self.add_tab()

        # Create toolbar
        self.create_toolbar()

        # Initialize tab search
        self.init_tab_search()

        # Load saved tab groups
        self.load_tab_groups()

        # Restore session
        self.restore_session()

    def init_database(self):
        self.conn = sqlite3.connect("browser_data.db")
        self.cursor = self.conn.cursor()
        
        # Create schema_version table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS schema_version
                             (version INTEGER PRIMARY KEY)''')
        
        # Get current schema version
        self.cursor.execute("SELECT version FROM schema_version")
        version = self.cursor.fetchone()
        if not version:
            version = 1
            self.cursor.execute("INSERT INTO schema_version (version) VALUES (?)", (version,))
        else:
            version = version[0]
        
        # Create or update tables based on version
        if version == 1:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS bookmarks
                                 (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, url TEXT)''')
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS history
                                 (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, url TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
            
            # Check if tab_groups table exists and its structure
            self.cursor.execute("PRAGMA table_info(tab_groups)")
            columns = [info[1] for info in self.cursor.fetchall()]
            
            if "tab_groups" not in [table[0] for table in self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")]:
                self.cursor.execute('''CREATE TABLE tab_groups
                                     (tab_id TEXT PRIMARY KEY, group_name TEXT, color TEXT)''')
            elif "tab_index" in columns and "tab_id" not in columns:
                self.cursor.execute('''CREATE TABLE tab_groups_new
                                     (tab_id TEXT PRIMARY KEY, group_name TEXT, color TEXT)''')
                self.cursor.execute('''INSERT INTO tab_groups_new (tab_id, group_name, color)
                                     SELECT CAST(tab_index AS TEXT), group_name, color FROM tab_groups''')
                self.cursor.execute('''DROP TABLE tab_groups''')
                self.cursor.execute('''ALTER TABLE tab_groups_new RENAME TO tab_groups''')
                self.cursor.execute("UPDATE schema_version SET version = 2")
                version = 2
        
        if version == 2:
            pass
        
        self.conn.commit()

    def create_toolbar(self):
        # Main toolbar
        self.toolbar = QToolBar("Navigation")
        self.toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # Menu button
        menu_btn = QAction(Icons.menu(), "Menu", self)
        menu_btn.setToolTip("Main Menu")
        menu_btn.triggered.connect(self.show_main_menu)
        self.toolbar.addAction(menu_btn)

        # Navigation buttons
        back_btn = QAction(Icons.back(), "Back", self)
        back_btn.setShortcut("Alt+Left")
        back_btn.triggered.connect(self.navigate_back)
        self.toolbar.addAction(back_btn)

        forward_btn = QAction(Icons.forward(), "Forward", self)
        forward_btn.setShortcut("Alt+Right")
        forward_btn.triggered.connect(self.navigate_forward)
        self.toolbar.addAction(forward_btn)

        reload_btn = QAction(Icons.reload(), "Reload", self)
        reload_btn.setShortcut("F5")
        reload_btn.triggered.connect(self.reload_page)
        self.toolbar.addAction(reload_btn)

        # Home button
        home_btn = QAction(Icons.home(), "Home", self)
        home_btn.setShortcut("Alt+Home")
        home_btn.triggered.connect(self.go_home)
        self.toolbar.addAction(home_btn)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search Google or type URL")
        self.url_bar.setClearButtonEnabled(True)
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)

        # Extensions spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.toolbar.addWidget(spacer)

        # Bookmarks button
        bookmark_btn = QAction(Icons.bookmarks(), "Bookmarks", self)
        bookmark_btn.setShortcut("Ctrl+D")
        bookmark_btn.triggered.connect(self.add_bookmark)
        self.toolbar.addAction(bookmark_btn)

        # Downloads button
        downloads_btn = QAction(Icons.downloads(), "Downloads", self)
        downloads_btn.setShortcut("Ctrl+J")
        downloads_btn.triggered.connect(self.show_downloads)
        self.toolbar.addAction(downloads_btn)

        # Dev tools button
        devtools_btn = QAction(Icons.devtools(), "DevTools", self)
        devtools_btn.setShortcut("Ctrl+Shift+I")
        devtools_btn.triggered.connect(self.toggle_dev_tools)
        self.toolbar.addAction(devtools_btn)

    def add_tab(self, url=None, incognito=False):
        browser_tab = BrowserTab(self, incognito)
        i = self.tabs.addTab(browser_tab, "New Tab")
        self.tabs.setCurrentIndex(i)
        
        browser_tab.urlChanged.connect(lambda url: self.update_tab_title(i, browser_tab))
        browser_tab.titleChanged.connect(lambda title: self.update_tab_title(i, browser_tab))
        
        if not incognito:
            browser_tab.urlChanged.connect(self.add_to_history)
        
        if url:
            browser_tab.browser.setUrl(QUrl(url))
        else:
            browser_tab.browser.setUrl(QUrl("https://www.google.com"))
        
        self.update_tab_style(i)
        return browser_tab

    def update_tab_title(self, index, browser_tab):
        title = browser_tab.browser.title()
        if not title:
            title = browser_tab.browser.url().toString()
            if title.startswith("https://"):
                title = title[8:]
            elif title.startswith("http://"):
                title = title[7:]
        
        self.tabs.setTabText(index, title[:20] + "..." if len(title) > 20 else title)
        self.update_tab_style(index)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            widget = self.tabs.widget(index)
            if widget:
                if widget.tab_id in self.tab_groups:
                    self.cursor.execute("DELETE FROM tab_groups WHERE tab_id = ?", (widget.tab_id,))
                    self.conn.commit()
                    del self.tab_groups[widget.tab_id]
                widget.deleteLater()
            self.tabs.removeTab(index)
            self.update_tab_styles()

    def navigate_back(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.browser.back()

    def navigate_forward(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.browser.forward()

    def reload_page(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.browser.reload()

    def go_home(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.navigate_to_url(self.url_bar.text())

    def add_bookmark(self):
        current_tab = self.tabs.currentWidget()
        if current_tab and not current_tab.incognito:
            try:
                url = current_tab.browser.url().toString()
                title = current_tab.browser.title() or url
                self.cursor.execute("INSERT INTO bookmarks (title, url) VALUES (?, ?)", (title, url))
                self.conn.commit()
                self.show_bookmark_animation()
            except sqlite3.Error as e:
                QMessageBox.warning(self, "Database Error", f"Failed to add bookmark: {str(e)}")

    def show_bookmark_animation(self):
        anim = AnimationPlayer(self)
        anim.load_animation("animations/success")
        anim.move(self.width() - 150, 50)
        anim.show()
        
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(2000, anim.deleteLater)

    def add_to_history(self, url):
        current_tab = self.tabs.currentWidget()
        if current_tab and not current_tab.incognito:
            try:
                title = current_tab.browser.title() or url
                self.cursor.execute("INSERT INTO history (title, url) VALUES (?, ?)", (title, url))
                self.conn.commit()
            except sqlite3.Error as e:
                logging.error(f"Failed to add to history: {str(e)}")

    def init_tab_search(self):
        self.tab_search_action = QAction("Search Tabs", self)
        self.tab_search_action.setShortcut("Ctrl+Shift+A")
        self.tab_search_action.triggered.connect(self.show_tab_search)
        self.addAction(self.tab_search_action)

    def show_tab_search(self):
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Search Tabs")
        dialog.setLabelText("Search open tabs:")
        
        tab_titles = [self.tabs.tabText(i) for i in range(self.tabs.count())]
        dialog.setComboBoxItems(tab_titles)
        dialog.setComboBoxEditable(True)
        
        if dialog.exec_():
            selected_text = dialog.textValue()
            for i in range(self.tabs.count()):
                if selected_text.lower() in self.tabs.tabText(i).lower():
                    self.tabs.setCurrentIndex(i)
                    break

    def group_tab(self):
        current_index = self.tabs.currentIndex()
        current_tab = self.tabs.widget(current_index)
        if not current_tab:
            return
        
        group_name, ok = QInputDialog.getText(self, "Tab Group", "Enter group name:")
        if ok and group_name:
            color = QColorDialog.getColor()
            if color.isValid():
                self.tab_groups[current_tab.tab_id] = (group_name, color.name())
                self.cursor.execute("INSERT OR REPLACE INTO tab_groups (tab_id, group_name, color) VALUES (?, ?, ?)",
                                   (current_tab.tab_id, group_name, color.name()))
                self.conn.commit()
                self.update_tab_style(current_index)

    def load_tab_groups(self):
        try:
            self.cursor.execute("SELECT tab_id, group_name, color FROM tab_groups")
            for tab_id, group_name, color in self.cursor.fetchall():
                self.tab_groups[tab_id] = (group_name, color)
                for i in range(self.tabs.count()):
                    tab = self.tabs.widget(i)
                    if tab and tab.tab_id == tab_id:
                        self.update_tab_style(i)
        except sqlite3.Error as e:
            logging.error(f"Failed to load tab groups: {str(e)}")

    def update_tab_style(self, index):
        tab = self.tabs.widget(index)
        if not tab or tab.tab_id not in self.tab_groups:
            self.tabs.tabBar().setTabTextColor(index, Qt.white)
            self.tabs.tabBar().setTabButton(index, QTabBar.LeftSide, None)
            return
        
        group_name, color = self.tab_groups[tab.tab_id]
        self.tabs.tabBar().setTabTextColor(index, color)
        
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        label = QLabel(group_name[0].upper())
        label.setStyleSheet(f"""
            QLabel {{
                color: white;
                background-color: {color};
                border-radius: 8px;
                padding: 2px 6px;
                font-weight: bold;
            }}
        """)
        layout.addWidget(label)
        
        title = QLabel(self.tabs.tabText(index))
        title.setStyleSheet("color: white;")
        layout.addWidget(title)
        layout.addStretch()
        
        widget.setLayout(layout)
        self.tabs.tabBar().setTabButton(index, QTabBar.LeftSide, widget)

    def update_tab_styles(self):
        for i in range(self.tabs.count()):
            self.update_tab_style(i)

    def toggle_dev_tools(self):
        current_tab = self.tabs.currentWidget()
        if current_tab:
            current_tab.toggle_dev_tools()

    def show_downloads(self):
        downloads_tab = self.add_tab("chrome://downloads", incognito=False)
        self.tabs.setTabText(self.tabs.currentIndex(), "Downloads")

    def show_main_menu(self):
        menu = QMenu(self)
        
        new_tab = QAction(Icons.new_tab(), "New Tab", self)
        new_tab.setShortcut("Ctrl+T")
        new_tab.triggered.connect(lambda: self.add_tab())
        menu.addAction(new_tab)
        
        new_incognito = QAction(Icons.incognito(), "New Incognito Tab", self)
        new_incognito.setShortcut("Ctrl+Shift+N")
        new_incognito.triggered.connect(lambda: self.add_tab(incognito=True))
        menu.addAction(new_incognito)
        
        menu.addSeparator()
        
        bookmarks_menu = QMenu("Bookmarks", self)
        self.update_bookmarks_menu(bookmarks_menu)
        menu.addMenu(bookmarks_menu)
        
        history_menu = QMenu("History", self)
        self.update_history_menu(history_menu)
        menu.addMenu(history_menu)
        
        menu.addSeparator()
        
        group_action = QAction("Group This Tab", self)
        group_action.triggered.connect(self.group_tab)
        menu.addAction(group_action)
        
        menu.addSeparator()
        
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        menu.addAction(settings_action)
        
        about_action = QAction("About Utharam", self)
        about_action.triggered.connect(self.show_about)
        menu.addAction(about_action)
        
        menu.addSeparator()
        
        clear_history_action = QAction("Clear History", self)
        clear_history_action.triggered.connect(self.clear_history)
        menu.addAction(clear_history_action)
        
        clear_bookmarks_action = QAction("Clear Bookmarks", self)
        clear_bookmarks_action.triggered.connect(self.clear_bookmarks)
        menu.addAction(clear_bookmarks_action)
        
        menu.exec_(self.mapToGlobal(self.toolbar.geometry().bottomLeft()))

    def update_bookmarks_menu(self, menu):
        menu.clear()
        try:
            self.cursor.execute("SELECT title, url FROM bookmarks ORDER BY id DESC LIMIT 20")
            for title, url in self.cursor.fetchall():
                action = QAction(title[:40], self)
                action.setToolTip(url)
                action.triggered.connect(lambda checked, u=url: self.add_tab(u))
                menu.addAction(action)
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Database Error", f"Failed to load bookmarks: {str(e)}")

    def update_history_menu(self, menu):
        menu.clear()
        try:
            self.cursor.execute("SELECT title, url, timestamp FROM history ORDER BY timestamp DESC LIMIT 20")
            for title, url, timestamp in self.cursor.fetchall():
                action = QAction(f"{title[:30]} - {url[:30]}", self)
                action.setToolTip(url)
                action.triggered.connect(lambda checked, u=url: self.add_tab(u))
                menu.addAction(action)
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Database Error", f"Failed to load history: {str(e)}")

    def show_settings(self):
        settings_dialog = SettingsDialog()
        settings_dialog.exec_()

    def show_about(self):
        about_dialog = AboutDialog()
        about_dialog.exec_()

    def save_session(self):
        session = []
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            session.append({
                "url": tab.browser.url().toString(),
                "title": self.tabs.tabText(i),
                "tab_id": tab.tab_id,
                "incognito": tab.incognito,
                "group": self.tab_groups.get(tab.tab_id, None)
            })
        try:
            with open("session.json", "w") as f:
                json.dump(session, f)
        except Exception as e:
            logging.error(f"Failed to save session: {str(e)}")

    def restore_session(self):
        try:
            with open("session.json", "r") as f:
                session = json.load(f)
            for tab_data in session:
                tab = self.add_tab(tab_data["url"], tab_data["incognito"])
                self.tabs.setTabText(self.tabs.indexOf(tab), tab_data["title"])
                if tab_data["group"]:
                    self.tab_groups[tab.tab_id] = tab_data["group"]
                    self.cursor.execute("INSERT OR REPLACE INTO tab_groups (tab_id, group_name, color) VALUES (?, ?, ?)",
                                       (tab.tab_id, tab_data["group"][0], tab_data["group"][1]))
            self.conn.commit()
            self.update_tab_styles()
        except FileNotFoundError:
            pass
        except Exception as e:
            logging.error(f"Failed to restore session: {str(e)}")

    def clear_history(self):
        try:
            self.cursor.execute("DELETE FROM history")
            self.conn.commit()
            QMessageBox.information(self, "History", "Browsing history cleared.")
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Failed to clear history: {str(e)}")

    def clear_bookmarks(self):
        try:
            self.cursor.execute("DELETE FROM bookmarks")
            self.conn.commit()
            QMessageBox.information(self, "Bookmarks", "Bookmarks cleared.")
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Failed to clear bookmarks: {str(e)}")

    def closeEvent(self, event):
        self.save_session()
        while self.tabs.count() > 0:
            widget = self.tabs.widget(0)
            if widget:
                widget.deleteLater()
            self.tabs.removeTab(0)
        self.conn.close()
        super().closeEvent(event)