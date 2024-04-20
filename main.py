import curses
import threading
import time
import copy

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
        self.enemies = []
        for i in range(6):
            self.enemy = [[i,0,"("],
                      [i,1,"@"],
                      [i,2,")"]]
            for j in range(11):
                self.enemies.append(copy.deepcopy(self.enemy))
                for k in self.enemy:
                    k[1] +=3
            self.enemy_shots = my_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.player1_shot = [0,0]

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
        for i in self.enemies:
            for r,c,ch in i:
                self.field[r][c] = str(ch)

    def controller(self,new_direction):
        # 1  2
        self.direction = new_direction
        
    def move_p1(self):
        diff = 0
        if self.direction == 1 and self.player1[0][1] > 0:
            diff = -1
        elif self.direction == 2 and self.player1[4][1] < COLUMNS-1:
            diff = 1
        else:
            diff = 0
        for i in self.player1:
            i[1] +=diff

    def move_enemy(self,chosen,x,y):
        for j in self.enemies[chosen]:
            j[0]=x
            j[1]=y

    
def controller(window, board):
    while not board.game_over:
        char = window.getch()
        if char == curses.KEY_LEFT:
            board.controller(1)
        elif char == curses.KEY_RIGHT:
            board.controller(2)
        else:
            board.controller(0)

def control_enemy(board, enemy):
    while not board.game_over:
        x_offset = 1 if enemy[0][1] < COLUMNS - 3 else -1  # Move right until near the edge, then left
        y_offset = 0 if enemy[0][1] < COLUMNS - 3 else 1  # Move downwards if near the edge
        print(f"Enemy {enemy} - x_offset: {x_offset}, y_offset: {y_offset}")
        board.move_enemy(enemy, x_offset, y_offset)
        time.sleep(0.1)

            
        

            

    
def start(window):
    board = Board()
    control_enemies = []
    control_p1 = threading.Thread(target=controller, args=(window, board))
    control_p1.start()
    for i, enemy in enumerate(board.enemies):
        thread = threading.Thread(target=control_enemy, args=(board, enemy))  # Pass individual enemy
        control_enemies.append(thread)
        thread.start()

    curses.curs_set(0)
    while not board.game_over:
        window.clear()
        window.insstr(0,0, str(board))
        window.refresh()
        time.sleep(0.1)

        board.move_p1()
        board.refresh()

    control_p1.join()
    for thread in control_enemy:
        thread.join()

if __name__ == "__main__":
    curses.wrapper(start)
