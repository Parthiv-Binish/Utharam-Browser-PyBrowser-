<!-- Custom pixel-style animated welcome banner in purple -->

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Press+Start+2P&size=20&duration=3000&pause=1000&center=true&vCenter=true&multiline=true&width=700&height=100&lines=WELCOME+TO+MY+WORLD!;Crafting+Code+With+Passion!&color=8000FF" />
</p>

<!-- Pixel-style animated banner -->

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=Hi%20I'm%20Parthiv%20Binish&fontSize=40&fontAlignY=35&desc=Creator%20of%20Utharam%20Browser%20|%20Educator%20%26%20Developer&descAlignY=60&descAlign=62" />
</p>

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=parthiv-binish&label=Profile%20views&color=0e75b6&style=flat" alt="profile views" />
  <img src="https://img.shields.io/badge/Welcome%20to%20my%20profile-Heart-pink" />
</p>

<h3 align="center">Turning Ideas into Scalable Solutions | Progressive Software Solutions & Training</h3>

---

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

### 🛠 Languages and Tools

<p align="left">
  <img src="https://skillicons.dev/icons?i=html,css,js,react,nodejs,express,mongodb,mysql,php,python,java,cpp,c,photoshop,sass,electron" />
</p>

---

## 📜 License

MIT License © 2025 Parthiv Binish
