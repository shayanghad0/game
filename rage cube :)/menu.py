import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel
)
from PyQt5.QtCore import Qt

class RageCubeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rage Cube")
        self.setFixedSize(400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.init_ui()
        self.apply_light_mode()

    def init_ui(self):
        # Header
        header_layout = QHBoxLayout()
        self.dark_mode_btn = QPushButton("🌙")
        self.light_mode_btn = QPushButton("☀️")
        exit_btn = QPushButton("❌")

        self.dark_mode_btn.clicked.connect(self.apply_dark_mode)
        self.light_mode_btn.clicked.connect(self.apply_light_mode)
        exit_btn.clicked.connect(self.close)

        for btn in [self.dark_mode_btn, self.light_mode_btn, exit_btn]:
            btn.setFixedSize(30, 30)
            header_layout.addWidget(btn)

        header_layout.addStretch()
        self.main_layout.addLayout(header_layout)

        # Body (center)
        body_layout = QVBoxLayout()
        body_layout.setAlignment(Qt.AlignCenter)

        welcome_label = QLabel("Welcome to Rage Cube")
        welcome_label.setObjectName("welcomeLabel")

        start_btn = QPushButton("Start")
        start_btn.setObjectName("startButton")

        body_layout.addWidget(welcome_label)
        body_layout.addWidget(start_btn)
        self.main_layout.addLayout(body_layout)

        # Footer
        footer_label = QLabel("Developed by Shayan Ghadamian")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setObjectName("footerLabel")
        self.main_layout.addWidget(footer_label)

    def apply_dark_mode(self):
        dark_css = """
        QWidget {
            background-color: #121212;
            color: #ffffff;
        }
        QPushButton {
            background-color: #2c2c2c;
            color: white;
            border-radius: 5px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #3a3a3a;
        }
        #welcomeLabel {
            font-size: 18px;
            font-weight: bold;
        }
        #startButton {
            margin-top: 10px;
            background-color: #5a5aff;
        }
        #footerLabel {
            font-size: 10px;
            color: #aaaaaa;
        }
        """
        self.setStyleSheet(dark_css)

    def apply_light_mode(self):
        light_css = """
        QWidget {
            background-color: #f0f0f0;
            color: #000000;
        }
        QPushButton {
            background-color: #e0e0e0;
            color: black;
            border-radius: 5px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #d0d0d0;
        }
        #welcomeLabel {
            font-size: 18px;
            font-weight: bold;
        }
        #startButton {
            margin-top: 10px;
            background-color: #4285f4;
            color: white;
        }
        #footerLabel {
            font-size: 10px;
            color: #555555;
        }
        """
        self.setStyleSheet(light_css)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RageCubeApp()
    window.show()
    sys.exit(app.exec_())
