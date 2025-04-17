import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QTextEdit
from PyQt5.QtCore import Qt

class RageCubeGuide(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rage Cube - Guide Page")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet(self.get_dark_theme())  # Start with dark mode

        # Layouts
        main_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        body_layout = QGridLayout()
        footer_layout = QHBoxLayout()

        # Header buttons (for mode switching and exit)
        self.dark_btn = QPushButton("🌙")
        self.light_btn = QPushButton("☀️")
        exit_btn = QPushButton("❌")
        home_btn = QPushButton("🏠⬅️")  # Back button to go back to lmenu.py

        self.dark_btn.clicked.connect(self.enable_dark_mode)
        self.light_btn.clicked.connect(self.enable_light_mode)
        exit_btn.clicked.connect(self.close)
        home_btn.clicked.connect(self.go_back_to_main_menu)  # Going back to lmenu.py

        for btn in [self.dark_btn, self.light_btn, exit_btn, home_btn]:
            btn.setFixedSize(40, 30)
            header_layout.addWidget(btn)

        header_layout.addStretch()

        # Body content (The buttons for each section)
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)  # Set text area to be read-only
        self.text_area.setFixedHeight(200)  # Set height for the text area

        average_man_btn = QPushButton("level 1-2-3")
        laser_man_btn = QPushButton("level 4-5-6")
        what_the_heck_btn = QPushButton("level 7-8-9")
        boss_fight_btn = QPushButton("Boss Fight")

        average_man_btn.clicked.connect(lambda: self.display_text("level 1-2-3"))
        laser_man_btn.clicked.connect(lambda: self.display_text("level 4-5-6"))
        what_the_heck_btn.clicked.connect(lambda: self.display_text("level 7-8-9"))
        boss_fight_btn.clicked.connect(lambda: self.display_text("Boss Fight"))

        # Set button styles
        for btn in [average_man_btn, laser_man_btn, what_the_heck_btn, boss_fight_btn]:
            btn.setFixedSize(150, 40)
            btn.setStyleSheet(self.get_button_style())

        # Add buttons to the body layout in grid fashion
        body_layout.addWidget(average_man_btn, 0, 0)
        body_layout.addWidget(laser_man_btn, 0, 1)
        body_layout.addWidget(what_the_heck_btn, 1, 0)
        body_layout.addWidget(boss_fight_btn, 1, 1)

        # Add text area to body layout
        body_layout.addWidget(self.text_area, 2, 0, 1, 2)

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

    def go_back_to_main_menu(self):
        """Go back to the main menu (lmenu.py)."""
        try:
            subprocess.Popen(["python", "lmenu.py"])  # Run lmenu.py script
            self.close()  # Close the guide window
        except FileNotFoundError:
            print("Error: lmenu.py not found!")

    def display_text(self, category):
        """Display the corresponding text for each category when clicked."""
        if category == "level 1-2-3":
            text = """
level 1-2-3:
Level 1: Simple Start
Objective:
Survive for 10 seconds.

This is your introductory level where the player gets used to basic movement.

Key Features:
Player Controls: Arrow keys to move.

Obstacles: Simple, slow-moving red blocks.

No gravity flip or teleportation: It's just you and the obstacles.

Survival time: 10 seconds to win.

Level 2: Adding More Obstacles
Objective:
Survive for 15 seconds while dealing with more obstacles.

Key Features:
Red Obstacles: More than 3 obstacles are moving on the screen.

Speed up obstacles: They’re a bit faster than before.

Survival Time: 15 seconds.

The player controls remain the same as in Level 1.

Level 3: Faster and Trickier
Objective:
Survive for 20 seconds while dealing with faster obstacles.

Key Features:
Obstacles: They’re moving faster.

More Obstacles: You’ll have at least 5 obstacles to dodge.

Teleporting Player: The player teleports every 3 seconds.

Survival Time: 20 seconds.

Player Controls: Arrow keys to move.
            """
        elif category == "level 4-5-6":
            text = """
level 4-5-6:
Level 4: Platform Movement
Objective:
Survive for 25 seconds while dodging moving platforms.

Key Features:
Obstacles: Still present, but the platforms are the real challenge.

Moving Platforms: Platforms will appear and move up and down, forcing you to jump between them.

Speeding Obstacles: The obstacles are now moving faster.

Survival Time: 25 seconds.

Player Controls: Arrow keys + WASD keys to move. You’ll need to jump between platforms!

Level 5: Gravity Flip
Objective:
Survive for 30 seconds with gravity flip mechanics.

Key Features:
Gravity Flip: Gravity will randomly flip, causing you to fall up instead of down.

Faster Obstacles: Obstacles now move much faster.

Platforms Move: Platforms still move, but with more variation.

Obstacles: Red obstacles become faster.

Survival Time: 30 seconds.

Level 6: Chasers
Objective:
Survive for 35 seconds while chasing enemies are added.

Key Features:
Chasers: Blue enemies that will follow the player’s position.

Obstacles: Red obstacles continue to fall.

Survival Time: 35 seconds.

Platforms: Moving platforms add more complexity to the level.

Player Controls: WASD + Arrow Keys (still).
            """
        elif category == "level 7-8-9":
            text = """
level 7-8-9??:
Level 7: Double Trouble
Objective:
Survive for 40 seconds while dodging double the obstacles and chasing enemies.

Key Features:
Double Obstacles: Twice as many obstacles will fall at random positions.

Chasers: Faster than before, and they’re coming after you with intent.

Teleporting: You will teleport every 2 seconds, adding more unpredictability.

Survival Time: 40 seconds.

Level 8: Bullet Hell
Objective:
Survive for 45 seconds while dodging laser attacks and chasing enemies.

Key Features:
Laser Barrage: Lasers that shoot from the top and bottom of the screen, coming towards the player.

Chasers: Even faster.

Obstacles: Still fall, but much faster.

Moving Platforms: Even more complicated with platforms appearing and disappearing.

Survival Time: 45 seconds.

Teleporting: Player still teleports at intervals.

Level 9: Chaos Unleashed
Objective:
Survive for 50 seconds while dealing with random teleportation, projectiles, and lasers.

Key Features:
Projectiles: Red projectiles shoot across the screen, chasing the player.

Teleporting Player: Every 3 seconds, the player teleports randomly to a different spot.

Boss Health: If you damage the boss, it gets weaker and you win after 50 seconds.

Obstacles: Spawn more rapidly.

Chasers: These enemies move in much faster patterns.

Survival Time: 50 seconds.
            """
        elif category == "Boss Fight":
            text = "Wait to complete the game levels to unlock Boss Fight details."

        self.text_area.setText(text)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RageCubeGuide()
    window.show()
    sys.exit(app.exec_())
