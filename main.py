import curses
import threading
import time

ROWS, COLUMNS = 25, 50

class Board:

    def __init__(self):
        self.lives = 3
        self.score = 0
        self.field = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

        self.player1 = [[ROWS-1,(int(COLUMNS/2)-2),"<"],
                        [ROWS-1,(int(COLUMNS/2)-1),"|"],
                        [ROWS-1,(int(COLUMNS/2)),"Y"],
                        [ROWS-1,(int(COLUMNS/2)+1),"|"],
                        [ROWS-1,(int(COLUMNS/2)+2),">"],
                        [ROWS-2,(int(COLUMNS/2)-1),"/"],
                        [ROWS-2,(int(COLUMNS/2)),"*"],
                        [ROWS-2,(int(COLUMNS/2)+1),"\\"]]
        self.direction = 0
        #self.enemies
        self.enemy_shots = my_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.player1_shot = [(0,0)]

        self.game_over = False

    def __str__(self):
        score = f"Score: {self.score}"
        hp = f"HP x {self.lives}"
        area = "|"+"=" * (COLUMNS-2) + "==|" + "\n"
        for row in self.field:
            area += "|"
            for slot in row:
                area += slot
            area += "|\n"
        area +="|" + hp + "=" * (COLUMNS-14) + score + "|"
        return area
    
    def refresh(self):
        self.field =[[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
        for r,c,ch in self.player1:
            self.field[r][c] = str(ch)

    def controller(self,new_direction):
        # 1  2
        self.direction = new_direction
    def move_p1(self):
        diff = 0
        if self.direction == 1:
            diff = -1
        elif self.direction == 2:
            diff = 1
        else:
            diff = 0
        for i in self.player1:
            i[1] +=diff
    
def controller(window, board):
    while not board.game_over:
        char = window.getch()
        if char == curses.KEY_LEFT:
            board.controller(1)
        elif char == curses.KEY_RIGHT:
            board.controller(2)
        else:
            board.controller(0)

            

    
def start(window):
    board = Board()

    control_p1 = threading.Thread(target=controller, args=(window, board))
    control_p1.start()
    curses.curs_set(0)
    while not board.game_over:
        window.clear()
        window.insstr(0,0, str(board))
        window.refresh()
        time.sleep(0.1)

        board.move_p1()
        board.refresh()

    control_p1.join()

if __name__ == "__main__":
    curses.wrapper(start)
