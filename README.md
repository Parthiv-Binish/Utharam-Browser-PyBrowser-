
# 🧭 Utharam Browser

**Utharam** is a modern, lightweight, Chromium-based custom web browser built with **PyQt5** and **QtWebEngine**. It is designed by **Parthiv Binish** for teaching GUI and web programming with rich features, clean design, and session management.

![Utharam Logo](logo.png)

---

## 🚀 Features

* 🔖 Bookmark & History Management
* 🕵️‍♂️ Incognito Browsing Mode
* 🧩 Tab Grouping with Colors
* 📁 Download Manager
* 🛠 Built-in Developer Tools
* 💾 Session Restore
* 🌐 Google Search Integration
* 🎨 Custom Toolbar & Animations
* 🖥 Settings Panel (e.g., JavaScript toggle)
* 🧪 Chromium-based Rendering via `QWebEngine`

---

## 📁 Project Structure

```bash
utharam-browser/
├── main.py               # Entry point
├── browser.py            # Main browser window
├── tab.py                # Browser tab logic (navigation, downloads)
├── about.py              # About dialog with animation
├── settings.py           # Settings panel (example: JavaScript toggle)
├── config.py             # Config values like GitHub URL
├── icons.py              # Icon loader
├── resources.py          # Lottie animation player (WebEngine based)
├── icons/                # SVG icons
├── animations/           # Lottie animation JSONs
├── resources/            # JS dependencies (e.g. lottie.min.js)
├── styles.qss            # Qt style sheet
├── logo.png              # App logo
├── session.json          # Auto-saved session
├── browser_data.db       # SQLite DB for history/bookmarks
```

---

## 🔧 Requirements

* Python 3.7+
* PyQt5
* PyQtWebEngine

### Install dependencies:

```bash
pip install PyQt5 PyQtWebEngine
```

---

## 🏃 Running the App

```bash
python main.py
```

---

## 🔨 Build as Executable

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile main.py
```

> Make sure to include essential folders: `icons/`, `animations/`, `resources/`, and `logo.png`

---

## ⚙️ Settings

Preferences are saved in `settings.json`. For example, enable/disable JavaScript via the GUI.

---

## 🧠 Educational Purpose

* GUI development with PyQt
* Web rendering via QtWebEngine
* Custom styles and animations
* SQLite integration
* Session and state management

---

## 📂 Database Structure

* `bookmarks (id, title, url)`
* `history (id, title, url, timestamp)`
* `tab_groups (tab_id, group_name, color)`
* `schema_version`

---

## 📎 GitHub

[🔗 Utharam on GitHub](https://github.com/Parthiv-Binish/Utharam-Browser-PyBrowser)

---

## 📜 License

MIT License © 2025 Parthiv Binish
