import curses
import threading
import time
import copy
import time
import random

ROWS, COLUMNS = 25, 50

class Board:

    def __init__(self):
        self.lives = 3
        self.score = 0
        self.elapsed_time = 0
        self.col_taken = [ False for _ in range(COLUMNS)]
        self.field = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.shot_hitbox = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]

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
        self.x_offset = 0
        self.shot_matrix = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.y_offset = 0
        self.char_l = ["/","(","^","<","]","/","<"]
        self.char_r = ["\\",")","^",">","[","\\",">"]
        self.condition_move = threading.Condition()
        self.lock_enemy_bullets_move = threading.Lock()
        self.lock_player_bullets_move = threading.Lock()
        self.lock_spawn_bullets = threading.Lock()
        for i in range(6):
            self.enemy = [[i,1,self.char_l[i]],
                      [i,2,"@"],
                      [i,3,self.char_r[i]]]
            for j in range(11):
                self.enemies.append(copy.deepcopy(self.enemy))
                for k in self.enemy:
                    k[1] +=3

        self.game_over = False

    def __str__(self):
        score = f'Score: {"{:02d}".format(self.score)}'
        hp = f"HP x {self.lives}"
        area = "|"+"=" * (COLUMNS-2) + "==|" + "\n"
        for row in self.field:
            area += "|"
            for slot in row:
                area += slot
            area += "|\n"
        minutes = int(self.elapsed_time // 60)
        seconds = int(self.elapsed_time % 60)
        area +="|" + hp + "=" * (COLUMNS-35) + "{:02d}:{:02d}".format(minutes, seconds) + "=" * (COLUMNS-35) + score + "|"
        return area
    
    def refresh(self):
        self.field =[[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.shot_hitbox = [[" " for _ in range(COLUMNS)] for _ in range(ROWS)]
        for r,c,ch in self.player1:
            self.shot_hitbox[r][c] = "p"
            self.field[r][c] = str(ch)
        for i in range(len(self.enemies)):
            for r,c,ch in self.enemies[i]:
                self.shot_hitbox[r][c] = i
                self.field[r][c] = str(ch)
        for i in range(len(self.shot_matrix)):
            for j in range(len(self.shot_matrix[i])):
                if not self.shot_matrix[i][j] == " " :
                    self.field[i][j] = str(self.shot_matrix[i][j])
        

    def controller(self,new_direction):
        # 1  2
        self.direction = new_direction

    def controller_enemy(self,x,y):
        self.x_offset = x
        self.y_offset = y
        
    def move_p1(self):
        diff = 0
        if self.direction == 1 and self.player1[0][1] > 0:
            diff = -1
        elif self.direction == 2 and self.player1[4][1] < COLUMNS-2:
            diff = 1
        else:
            diff = 0
        for i in self.player1:
            i[1] +=diff

    def move_enemy(self):
        for enemy in self.enemies:
            i = 0
            for j in enemy:
                j[0]+=(self.x_offset)
                j[1]+=(self.y_offset)
                i+=1

    def shoot_p1(self):
        x_pos = self.player1[2][1]
        self.shot_matrix[ROWS-3][x_pos] = "|"

    def spawn_enemy_bullet(self):
        treshold = 0.9
        for enemy in self.enemies:
            if not self.shot_matrix[enemy[1][0]+1][enemy[1][1]] == "!" and self.field[enemy[1][0]+1][enemy[1][1]] == " ":
                if self.field[enemy[1][0]+1][enemy[1][1]] == " " and treshold <= random.random():
                    #self.shot_matrix[enemy[1][0]+1][enemy[1][1]] = "!"
                    control_bullet = threading.Thread(target=self.move_bullet,args=(enemy[1][0]+1, enemy[1][1]))
                    control_bullet.start()
                    #self.col_taken[enemy[1][1]] = True

    def move_bullet(self,i,j):
        while i+1 <= 24:
            self.shot_matrix[i][j] = " "
            if not self.field[i+1][j] == " " and self.shot_hitbox[i+1][j] == "p":
                self.shot_player()
                self.shot_matrix[i+1][j] = " "
            else:
                self.shot_matrix[i+1][j] = "!"
            i+=1
            time.sleep(0.1)
        self.shot_matrix[i][j] = " "


    def shot_enemy(self, x, y):
        self.enemies.pop(self.shot_hitbox[x][y])
        self.score+=1
    
    def shot_player(self):
        self.lives-=1
        if self.lives == 0:
            self.game_over = True
    
    def move_player_bullets(self):
        with self.lock_player_bullets_move:
            for i in range(len(self.shot_matrix)):
                for j in range(len(self.shot_matrix[i])):
                    if self.shot_matrix[i][j] == "|":
                        self.shot_matrix[i][j] = " "
                        if i-1 >= 1:
                            if not self.field[i-1][j] == " " and not self.field[i-1][j] == "!":
                                self.shot_enemy(i-1,j)
                                self.shot_matrix[i-1][j] = " "
                            else:
                                self.shot_matrix[i-1][j] = "|"

    
def controller(window, board):
    prev_char = 0
    while not board.game_over:
        char = window.getch()
        if char == curses.KEY_LEFT:
            board.controller(1)
        elif char == curses.KEY_RIGHT:
            board.controller(2)
        elif char == curses.KEY_UP and prev_char != curses.KEY_UP:
            board.shoot_p1()
        else:
            board.controller(0)
        prev_char = char

def controller_enemy(board, enemy):
    x_off = 0
    par = 1
    y_off = 0
    i = 0
    while not board.game_over:
        if par % 3 == 0:
            row_pos = enemy[0][0]
            if row_pos == 20:
                board.game_over = True
            if i == 0:
                x_off = 1
                y_off = 1
            elif i == 16:
                y_off = 1
                x_off = -1
            board.controller_enemy(y_off, x_off)
            if x_off == 1:
                i+=1
            elif x_off == -1:
                i-=1
            y_off = 0
        else:
            board.controller_enemy(0,0)
        par+=1
        time.sleep(0.1)

def controller_player_bullets(board):
    while not board.game_over:
        board.move_player_bullets()
        time.sleep(0.1)

def controller_enemy_bullets(board):
    while not board.game_over:
        board.move_enemy_bullets()
        time.sleep(0.1)



def spawn_enemy_shot(board):
    time.sleep(0.2)
    while not board.game_over:
        board.spawn_enemy_bullet()
        time.sleep(0.1)

def timer(board):
    while not board.game_over:
        board.elapsed_time+=1
        time.sleep(1.0)

    
def start(window):
    board = Board()
    control_enemies = []
    control_p1 = threading.Thread(target=controller, args=(window, board))
    control_p1.start()
    for i in board.enemies:
        control_enemy = threading.Thread(target=controller_enemy,args=(board, i))
        control_enemies.append(control_enemy)
        control_enemy.start()

    control_time = threading.Thread(target=timer, args=(board, ))
    control_time.start()

    control_spawn_enemy_bullets = threading.Thread(target=spawn_enemy_shot, args=(board, ))
    control_spawn_enemy_bullets.start()

    control_player_bullets = threading.Thread(target=controller_player_bullets, args=(board, ))
    control_player_bullets.start()

    curses.curs_set(0)
    while not board.game_over:
        window.clear()
        window.insstr(0,0, str(board))
        window.refresh()
        time.sleep(0.1)

        board.move_p1()
        board.move_enemy()
        board.refresh()

    control_p1.join()
    for thread in control_enemies:
        thread.join()
    control_player_bullets.join()
    control_time.join()
    control_spawn_enemy_bullets.join()

if __name__ == "__main__":
    curses.wrapper(start)
