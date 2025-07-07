from PyQt5.QtCore import Qt, QUrl, QSize, QDir
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AnimationPlayer(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(QSize(100, 100))
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.page().setBackgroundColor(Qt.transparent)
    
    def load_animation(self, animation_path):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, f"{animation_path}.json")
        lottie_path = os.path.join(base_dir, "resources", "lottie.min.js")
        
        # Convert paths to use forward slashes for web compatibility
        full_path = full_path.replace('\\', '/')
        lottie_path = lottie_path.replace('\\', '/')
        
        if not os.path.exists(full_path):
            logging.error(f"Animation file not found: {full_path}")
            self.setHtml("<div>Animation not available</div>")
            return
        
        if not os.path.exists(lottie_path):
            logging.error(f"Lottie library not found: {lottie_path}")
            self.setHtml("<div>Lottie library not available</div>")
            return
        
        logging.info(f"Loading animation from {full_path} with Lottie library {lottie_path}")
        
        self.setHtml(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="file:///{lottie_path}"></script>
            <style>
                body {{ margin: 0; background: transparent; }}
                #animation {{ width: 100%; height: 100%; }}
            </style>
        </head>
        <body>
            <div id="animation"></div>
            <script>
                try {{
                    if (typeof lottie !== 'undefined') {{
                        var animation = lottie.loadAnimation({{
                            container: document.getElementById('animation'),
                            renderer: 'svg',
                            loop: true,
                            autoplay: true,
                            path: 'file:///{full_path}'
                        }});
                    }} else {{
                        document.getElementById('animation').innerText = 'Lottie library not loaded';
                    }}
                }} catch (e) {{
                    document.getElementById('animation').innerText = 'Error loading animation: ' + e.message;
                }}
            </script>
        </body>
        </html>
        """)