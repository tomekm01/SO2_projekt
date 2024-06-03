# Spacja Najeźdźcy

This is a simple ASCII space invaders game implemented in Python using the curses library to present capabiliteis of multithreading.

## How to Play

1. Use the left and right arrow keys to move your spaceship.
2. Press the up arrow key to shoot bullets.
3. Avoid enemy bullets and eliminate all enemies to win.
4. You have three lives, and the game ends when you lose all lives.

## Installation

1. Clone this repository to your local machine.
2. Ensure you have Python 3.x installed.
3. Install the curses library if not already installed:
```bash
pip3 install curses
```
4. Run the game using the following command:
```bash
python3 main.py
```

## Controls
Due to curses limitations you cannot press the same button twice in a row.
- Left Arrow: Move spaceship left
- Right Arrow: Move spaceship right
- Up Arrow: Shoot bullets
- Down Arrow: Stop spaceship movement

## Game Features

- ASCII graphics for a retro gaming experience.
- Dynamic enemy movement.
- Player and enemy bullet collision detection.
- Score and remaining lives display.

## Multi-Threading

This project utilizes multiple threads to handle various aspects of the game concurrently. Each thread is responsible for different functionalities, such as player control, enemy movement, bullet management, and timing.

### Threads
- control_p1: Thread managing player input and movement.
- control_enemies: List of threads, each managing the movement of individual enemy units.
- control_time: Thread tracking elapsed game time.
- control_spawn_enemy_bullets: Thread spawning bullets fired by enemy units.
- control_player_bullets: Thread managing player bullet movement.
- Main thread: Controls the game loop and display updates.




## Credits

- This game is inspired by classic space invaders games.
- Implemented by Paweł Cyganiuk and Tomasz Mondrzycki.