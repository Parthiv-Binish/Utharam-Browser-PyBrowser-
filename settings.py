from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QCheckBox, QMessageBox
import json

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Utharam Browser Settings")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Example settings
        title = QLabel("<h2>Settings</h2>")
        layout.addWidget(title)
        
        # JavaScript toggle
        self.js_toggle = QCheckBox("Enable JavaScript")
        self.js_toggle.setChecked(True)
        layout.addWidget(self.js_toggle)
        
        # Save button
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
    
    def save_settings(self):
        try:
            settings = {"javascript_enabled": self.js_toggle.isChecked()}
            with open("settings.json", "w") as f:
                json.dump(settings, f)
            QMessageBox.information(self, "Settings", "Settings saved successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save settings: {str(e)}")