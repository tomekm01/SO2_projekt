import curses
import threading
import time

ROWS, COLUMNS = 50, 50

class Board:

    def __init__(self):
        self.lives = 3
        self.field = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

        self.player1 = [(1,COLUMNS/2)]
        self.enemies = [(11, 5)]
        self.enemy_shots = [(11)]
        self.player1_shot = False

        self.game_over = False

    def __str__(self):
        lives = f"HP x {self.lives}"
        area = "=" * COLUMNS + "\n"
        for row in self.field:
            area += "="
            for slot in row:
                area += slot
            area += "|\n"
        area += "#" * COLUMNS
        return area
    
    def refresh(self):
        self.field =[[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
    
def start(window):
    board = Board()
    while not board.game_over:
        window.clear()
        window.insstr(0,0, str(board))
        window.refresh()
        time.sleep(0.2)

        board.refresh()

if __name__ == "__main__":
    curses.wrapper(start)
