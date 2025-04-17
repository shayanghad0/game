# 🔥 RageCube: The Ultimate Rage Game

Welcome to **RageCube**, a minimal but brutally hard platformer game made with Python and Pygame. Survive, dodge, teleport, and rage your way through **10 intense levels**, each harder than the last — culminating in an epic **boss fight**!

---

## 🎮 Game Features

- 🔺 **Simple Controls** – Just arrow keys or WASD to move!
- 🧠 **Progressive Difficulty** – Each level introduces new mechanics.
- 🔴 **Deadly Obstacles** – Dodge red blocks, lasers, chasers, and more.
- 🌀 **Teleportation & Gravity Flips** – Random mechanics keep you on your toes.
- ⚔️ **Epic Boss Fight** – Face off in the final level against the ultimate enemy.
- 💾 **Save System** – Your progress is stored in `pass.json`.

---

## 📦 Installation

1. Make sure you have **Python 3.10+** installed.
2. Install `pygame` if you haven’t already:

```bash
pip install pygame
```

3. Clone or download this repository.

---

## ▶️ How to Play

```bash
python lmenu.py
```

- Start from level 1 and unlock each next level by surviving.
- Each level is a **10-50 second challenge**.
- Obstacles will **increase in speed and complexity** as you progress.
- Reach level 10 and defeat the **boss** to beat the game!

---

## 🧩 Level Breakdown

| Level | Challenge Type                | Survival Time |
|-------|-------------------------------|----------------|
| 1     | Basic Dodge                   | 10 seconds     |
| 2     | More/Faster Obstacles         | 15 seconds     |
| 3     | Teleportation                 | 20 seconds     |
| 4     | Moving Platforms              | 25 seconds     |
| 5     | Gravity Flip                  | 30 seconds     |
| 6     | Chasing Enemies               | 35 seconds     |
| 7     | Double Obstacles + Chasers    | 40 seconds     |
| 8     | Laser Attacks + Platforms     | 45 seconds     |
| 9     | Chaos Mode + Projectiles      | 50 seconds     |
| 10    | ⚔️ Boss Fight                 | 40 seconds     |

---

## 💾 Save Progress

Game progress is stored in a `pass.json` file like this:

```json
{
  "level_1": true,
  "level_2": true,
  "level_3": false,
  ...
}
```

---

## 🛠 Project Structure

```
ragecube/
├── lmenu.py          # Main menu script
├── level1.py         # Each level file
├── level2.py
├── ...
├── boss.py           # Final boss level
├── pass.json         # Save file
├── assets/           # Images, sounds, fonts (optional)
└── README.md         # You're here!
```

---

## 📌 Credits

- Built with ❤️ using **Python** and **Pygame**
- Idea & code by [Your Name or Handle]

---

## ⚠️ Warning

This game is designed to make you **rage**. Play at your own risk 😈

---

## 🏁 License

MIT License – free to use and modify.
```
