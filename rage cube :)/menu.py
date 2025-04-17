import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QStackedLayout
)
from PyQt5.QtCore import Qt


class RageCubeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rage Cube")
        self.setGeometry(100, 100, 500, 300)
        self.setStyleSheet(self.get_dark_theme())  # Start with dark mode

        # Layouts
        main_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        body_layout = QVBoxLayout()
        footer_layout = QHBoxLayout()

        # Header buttons
        self.dark_btn = QPushButton("🌙")
        self.light_btn = QPushButton("☀️")
        exit_btn = QPushButton("❌")

        self.dark_btn.clicked.connect(self.enable_dark_mode)
        self.light_btn.clicked.connect(self.enable_light_mode)
        exit_btn.clicked.connect(self.close)

        for btn in [self.dark_btn, self.light_btn, exit_btn]:
            btn.setFixedSize(40, 30)
            header_layout.addWidget(btn)

        header_layout.addStretch()

        # Body content
        title = QLabel("Welcome to Rage Cube")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("TitleLabel")

        start_btn = QPushButton("Start")
        start_btn.setFixedSize(120, 40)
        start_btn.clicked.connect(self.open_lmenu)

        body_layout.addWidget(title)
        body_layout.addSpacing(20)
        body_layout.addWidget(start_btn, alignment=Qt.AlignCenter)
        body_layout.addStretch()

        # Footer
        footer_label = QLabel("Developed by Shayan Ghadamian")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_layout.addWidget(footer_label)

        # Combine all layouts
        main_layout.addLayout(header_layout)
        main_layout.addLayout(body_layout)
        main_layout.addLayout(footer_layout)
        self.setLayout(main_layout)

    def enable_dark_mode(self):
        self.setStyleSheet(self.get_dark_theme())

    def enable_light_mode(self):
        self.setStyleSheet(self.get_light_theme())

    def open_lmenu(self):
        subprocess.Popen(["python", "lmenu.py"])
        self.close()

    def get_dark_theme(self):
        return """
        QWidget {
            background-color: #121212;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
        }
        QPushButton {
            background-color: #1f1f1f;
            border: 2px solid #555;
            border-radius: 10px;
            padding: 5px;
            color: #fff;
        }
        QPushButton:hover {
            background-color: #333;
        }
        QLabel#TitleLabel {
            font-size: 24px;
            font-weight: bold;
        }
        """

    def get_light_theme(self):
        return """
        QWidget {
            background-color: #f5f5f5;
            color: #000;
            font-family: 'Segoe UI', sans-serif;
        }
        QPushButton {
            background-color: #e0e0e0;
            border: 2px solid #aaa;
            border-radius: 10px;
            padding: 5px;
            color: #000;
        }
        QPushButton:hover {
            background-color: #d5d5d5;
        }
        QLabel#TitleLabel {
            font-size: 24px;
            font-weight: bold;
        }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RageCubeApp()
    window.show()
    sys.exit(app.exec_())
