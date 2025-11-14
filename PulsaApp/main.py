import os
import sys
import time
import random
import select
import termios, tty

# ------------------------------
# Game Settings
WIDTH = 40
HEIGHT = 15

# Player positions: Player1 bottom, Player2 top (can be controlled by another human)
player1_pos = [WIDTH//2, HEIGHT-1]
player2_pos = [WIDTH//2, 0]
ball_pos = [WIDTH//2, HEIGHT//2]

score1 = 0
score2 = 0

# Coach instruction
instruction = "Welcome to Pulsa Football!"

# Draw the ASCII field
def draw_field():
    os.system('clear')
    for y in range(HEIGHT):
        line = ''
        for x in range(WIDTH):
            if [x,y] == player1_pos:
                line += 'A'
            elif [x,y] == player2_pos:
                line += 'B'
            elif [x,y] == ball_pos:
                line += 'O'
            elif y == 0 or y == HEIGHT-1:
                line += '-'
            elif x == 0 or x == WIDTH-1:
                line += '|'
            else:
                line += ' '
        print(line)
    print(f"Score: Player1 {score1} - Player2 {score2}")
    print(f"Coach: {instruction}")

# Move ball with simple physics
def move_ball():
    global ball_pos, score1, score2, instruction
    dx = random.choice([-1,0,1])
    dy = random.choice([-1,0,1])
    ball_pos[0] += dx
    ball_pos[1] += dy

    # Keep ball in bounds
    if ball_pos[0] <= 1: ball_pos[0] = 1
    if ball_pos[0] >= WIDTH-2: ball_pos[0] = WIDTH-2
    if ball_pos[1] <= 0:
        score1 += 1
        ball_pos[0], ball_pos[1] = WIDTH//2, HEIGHT//2
        instruction = "GOAL Player1!"
        time.sleep(1)
    if ball_pos[1] >= HEIGHT-1:
        score2 += 1
        ball_pos[0], ball_pos[1] = WIDTH//2, HEIGHT//2
        instruction = "GOAL Player2!"
        time.sleep(1)

# Smarter AI for single human player mode
def ai_move():
    global instruction
    if ball_pos[0] < player2_pos[0]:
        player2_pos[0] -= 1
    elif ball_pos[0] > player2_pos[0]:
        player2_pos[0] += 1
    if ball_pos[1] < player2_pos[1]:
        player2_pos[1] -= 1
    elif ball_pos[1] > player2_pos[1]:
        player2_pos[1] += 1

# Non-blocking key press detection
def getch():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    return ch

# Player kick function
def kick_ball(player_pos):
    global ball_pos, instruction
    # Kick ball in the direction away from player
    if player_pos[1] < HEIGHT//2:  # top player
        ball_pos[1] += 1
    else:  # bottom player
        ball_pos[1] -= 1
    # Slight random horizontal kick
    ball_pos[0] += random.choice([-1,0,1])
    instruction = "Ball kicked!"

print("Controls: Player1 w/a/s/d + kick 'e', Player2 i/j/k/l + kick 'o'. Ctrl+C to quit.")
time.sleep(1)

while True:
    draw_field()
    move_ball()
    ai_move()  # AI can be disabled if two humans

    # Player input with timeout 0.3s per frame
    start_time = time.time()
    while time.time() - start_time < 0.3:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            ch = getch()
            # Player1 controls
            if ch == 'w' and player1_pos[1] > HEIGHT//2: player1_pos[1] -= 1
            elif ch == 's' and player1_pos[1] < HEIGHT-2: player1_pos[1] += 1
            elif ch == 'a' and player1_pos[0] > 1: player1_pos[0] -= 1
            elif ch == 'd' and player1_pos[0] < WIDTH-2: player1_pos[0] += 1
            elif ch == 'e': kick_ball(player1_pos)
            # Player2 controls
            elif ch == 'i' and player2_pos[1] < HEIGHT//2: player2_pos[1] += 1
            elif ch == 'k' and player2_pos[1] > 1: player2_pos[1] -= 1
            elif ch == 'j' and player2_pos[0] > 1: player2_pos[0] -= 1
            elif ch == 'l' and player2_pos[0] < WIDTH-2: player2_pos[0] += 1
            elif ch == 'o': kick_ball(player2_pos)
