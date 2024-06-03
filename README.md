# Spacja Najeźdźcy

The project is a space invaders-style game implemented in Python using the curses library for terminal-based graphics. It features multithreading to manage various game aspects simultaneously.

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
## Gameplay
![gameplay example](https://github.com/tomekm01/SO2_projekt/blob/main/gameplay_screenshot.PNG)



## Controls
Due to curses limitations you cannot press the same button twice in a row.
- Left Arrow - Move spaceship left
- Right Arrow - Move spaceship right
- Up Arrow - Shoot bullets
- Down Arrow - Stop spaceship movement

## Multi-Threading

This project utilizes multiple threads to handle various aspects of the game concurrently. Each thread is responsible for different functionalities, such as player control, enemy movement, bullet management, and timing.

### Threads
- `control_p1` - Thread managing player input and movement.
- `control_enemies` - List of threads, each managing the movement of individual enemy units.
- `control_time` - Thread tracking elapsed game time.
- `control_spawn_enemy_bullets` - Thread spawning bullets fired by enemy units.
- `control_player_bullets` - Thread managing player bullet movement.
- Main thread - Controls the game loop and display updates.

### Critical Sections
- Player Movement and Input - Controlled by the `controller()` function, which manages the direction of the player's movement based on user input.
- Enemy Movement - Managed by the `controller_enemy()` function, ensuring that enemy units move in a coordinated manner without conflicts.
- Player Bullet Movement - Handled by the `controller_player_bullets()` function, ensuring that player bullets move without interference from other actions.
- Enemy Bullet Spawning - Managed by the `spawn_enemy_shot()` function, ensuring that enemy bullets are spawned safely without race conditions.



## Credits

- This game is inspired by classic space invaders games.
- Implemented by Paweł Cyganiuk and Tomasz Mondrzycki.