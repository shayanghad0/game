import sys
import subprocess
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, 
    QHBoxLayout, QGridLayout
)
from PyQt5.QtCore import Qt

class RageCubeLMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rage Cube - Level Menu")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet(self.get_dark_theme())  # Start with dark mode

        # Load progress from JSON
        self.progress = self.load_progress()

        # Layouts
        main_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        body_layout = QGridLayout()
        footer_layout = QHBoxLayout()

        # Header buttons
        self.dark_btn = QPushButton("🌙")
        self.light_btn = QPushButton("☀️")
        exit_btn = QPushButton("❌")
        guide_btn = QPushButton("📘")  # New Guide Button

        self.dark_btn.clicked.connect(self.enable_dark_mode)
        self.light_btn.clicked.connect(self.enable_light_mode)
        exit_btn.clicked.connect(self.close)
        guide_btn.clicked.connect(self.open_guide)  # Connect to the new method

        # Set fixed size and add buttons to header
        for btn in [self.dark_btn, self.light_btn, exit_btn, guide_btn]:
            btn.setFixedSize(40, 30)
            header_layout.addWidget(btn)

        header_layout.addStretch()

        # Body content (Level buttons and Boss Fight button)
        level_buttons = []
        for i in range(1, 10):
            level_btn = QPushButton(f"Level {i}")
            level_btn.setFixedSize(120, 40)
            level_btn.setStyleSheet(self.get_button_style())
            
            # Disable button if previous level isn't passed
            if i > 1 and not self.progress[f"level_{i-1}"]:
                level_btn.setEnabled(False)
            
            level_btn.clicked.connect(lambda _, i=i: self.open_level(i))  # Lambda to pass the level number
            level_buttons.append(level_btn)
            body_layout.addWidget(level_btn, (i-1)//3, (i-1)%3)

        boss_fight_btn = QPushButton("Boss Fight")
        boss_fight_btn.setFixedSize(180, 50)
        boss_fight_btn.setStyleSheet(self.get_boss_button_style())
        boss_fight_btn.clicked.connect(self.open_boss_fight)

        body_layout.addWidget(boss_fight_btn, 3, 1)  # Centered below levels

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

    def open_level(self, level_num):
        """Open the corresponding level script when a level button is clicked."""
        level_file = f"level{level_num}.py"
        try:
            subprocess.Popen(["python", level_file])
            self.level_completed(level_num)  # Mark level as completed when it's opened
        except FileNotFoundError:
            print(f"Error: {level_file} not found!")

    def level_completed(self, level_num):
        """Mark a level as completed in the progress JSON file."""
        self.progress[f"level_{level_num}"] = True
        self.save_progress()  # Save the updated progress

    def save_progress(self):
        """Save the current progress to the pass.json file."""
        with open("pass.json", "w") as f:
            json.dump(self.progress, f)

    def load_progress(self):
        """Load the progress from the pass.json file."""
        try:
            with open("pass.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            # If pass.json doesn't exist, initialize with all levels as not completed
            return {
                "level_1": False,
                "level_2": False,
                "level_3": False,
                "level_4": False,
                "level_5": False,
                "level_6": False,
                "level_7": False,
                "level_8": False,
                "level_9": False
            }

    def open_guide(self):
        """Open the game guide script when the 'Guide' button is clicked."""
        try:
            subprocess.Popen(["python", "guid.py"])  # Launch the guide.py script
        except FileNotFoundError:
            print("Error: guid.py not found!")

    def open_boss_fight(self):
        """Open the boss fight script (you can create a boss fight script later)."""
        print("Boss fight triggered!")  # Placeholder for boss fight script
        # You can replace this with subprocess.Popen(["python", "boss_fight.py"])

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
        QPushButton:focus {
            border: 2px solid #00ff00;
        }
        QLabel {
            color: #fff;
            font-size: 14px;
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
        QPushButton:focus {
            border: 2px solid #00ff00;
        }
        QLabel {
            color: #000;
            font-size: 14px;
        }
        """

    def get_button_style(self):
        return """
        QPushButton {
            background-color: #2c3e50;
            border: 2px solid #34495e;
            border-radius: 8px;
            padding: 5px;
            color: white;
            font-weight: bold;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: #34495e;
        }
        QPushButton:focus {
            border: 2px solid #3498db;
        }
        """

    def get_boss_button_style(self):
        return """
        QPushButton {
            background-color: #e74c3c;
            border: 2px solid #c0392b;
            border-radius: 12px;
            padding: 10px;
            color: white;
            font-weight: bold;
            font-size: 18px;
        }
        QPushButton:hover {
            background-color: #c0392b;
        }
        QPushButton:focus {
            border: 2px solid #f39c12;
        }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RageCubeLMenu()
    window.show()
    sys.exit(app.exec_())
