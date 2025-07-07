import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDir
from browser import Browser
import sys

def ensure_resources():
    # Get the base directory of the application
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create necessary directories
    for folder in ["animations", "icons", "resources"]:
        QDir().mkpath(os.path.join(base_dir, folder))
    
    # Check for required files
    required_files = [
        os.path.join(base_dir, "styles.qss"),
        os.path.join(base_dir, "icons", "app_icon.svg"),
        os.path.join(base_dir, "animations", "success.json"),
        os.path.join(base_dir, "animations", "loading.json"),
        os.path.join(base_dir, "resources", "lottie.min.js"),
        os.path.join(base_dir, "logo.png")
    ]
    
    # Collect missing files
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    # Create default styles.qss if missing
    if not os.path.exists(os.path.join(base_dir, "styles.qss")):
        with open(os.path.join(base_dir, "styles.qss"), "w") as f:
            f.write("/* Default styles will be generated here */")
    
    return missing_files

if __name__ == "__main__":
    # Initialize QApplication first
    app = QApplication(sys.argv)
    app.setApplicationName("Utharam Browser")
    app.setApplicationDisplayName("Utharam Browser")
    app.setWindowIcon(QIcon(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons/app_icon.svg")))

    # Check resources and display warnings if any
    missing_files = ensure_resources()
    if missing_files:
        QMessageBox.warning(None, "Missing Resources",
                           f"The following resources are missing:\n{', '.join(missing_files)}\n"
                           "The application may not function correctly.")
    
    # Load styles
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "styles.qss"), "r") as file:
        app.setStyleSheet(file.read())

    window = Browser()
    window.show()
    
    sys.exit(app.exec_())