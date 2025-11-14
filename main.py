import pygame
import sys
import random
import array
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pulsa-App Football")

# Colors
GREEN = (0,128,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Players
player_size = 50
player_speed = 6
player1_pos = [WIDTH//2 - 100, HEIGHT - 100]
player2_pos = [WIDTH//2 + 100, 100]

# Ball
ball_radius = 20
ball_pos = [WIDTH//2, HEIGHT//2]
ball_speed = [5, -5]

# Scores
score1 = 0
score2 = 0
font = pygame.font.SysFont(None, 36)

# Coach instructions
instruction = "Welcome to Pulsa Football!"

# Generate beep sounds in-memory
def create_beep(frequency=440, duration_ms=150, volume=0.3):
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    buf = array.array("h", [int(volume*32767*math.sin(2*math.pi*frequency*t/sample_rate)) for t in range(n_samples)])
    sound = pygame.mixer.Sound(buffer=buf)
    return sound

kick_sound = create_beep(600, 100)
goal_sound = create_beep(400, 500)
crowd_sound = create_beep(800, 300)

# Field
goal_width = 200

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player1_pos[0] > 0:
        player1_pos[0] -= player_speed
        instruction = "Move Left"
    if keys[pygame.K_RIGHT] and player1_pos[0] < WIDTH - player_size:
        player1_pos[0] += player_speed
        instruction = "Move Right"
    if keys[pygame.K_UP] and player1_pos[1] > HEIGHT//2:
        player1_pos[1] -= player_speed
        instruction = "Move Up"
    if keys[pygame.K_DOWN] and player1_pos[1] < HEIGHT - player_size:
        player1_pos[1] += player_speed
        instruction = "Move Down"

    # Simple AI for player2
    if player2_pos[0] + player_size/2 < ball_pos[0]:
        player2_pos[0] += player_speed * 0.8
    if player2_pos[0] + player_size/2 > ball_pos[0]:
        player2_pos[0] -= player_speed * 0.8

    # Move ball
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Ball collision with walls
    if ball_pos[0] <= ball_radius or ball_pos[0] >= WIDTH - ball_radius:
        ball_speed[0] *= -1
    if ball_pos[1] <= ball_radius or ball_pos[1] >= HEIGHT - ball_radius:
        ball_speed[1] *= -1

    # Collision with players
    def check_collision(player_pos):
        px, py = player_pos
        return (px < ball_pos[0] < px+player_size and py < ball_pos[1] < py+player_size)
    if check_collision(player1_pos) or check_collision(player2_pos):
        ball_speed[1] *= -1
        kick_sound.play()
        instruction = "Kick!"

    # Check goals
    if ball_pos[1] <= 0:
        score1 += 1
        ball_pos = [WIDTH//2, HEIGHT//2]
        ball_speed = [random.choice([-5,5]), 5]
        goal_sound.play()
        crowd_sound.play()
        instruction = "GOAL Player 1!"
    elif ball_pos[1] >= HEIGHT:
        score2 += 1
        ball_pos = [WIDTH//2, HEIGHT//2]
        ball_speed = [random.choice([-5,5]), -5]
        goal_sound.play()
        crowd_sound.play()
        instruction = "GOAL Player 2!"

    # Draw field
    screen.fill(GREEN)
    pygame.draw.rect(screen, WHITE, (player1_pos[0], player1_pos[1], player_size, player_size))
    pygame.draw.rect(screen, RED, (player2_pos[0], player2_pos[1], player_size, player_size))
    pygame.draw.circle(screen, BLACK, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    pygame.draw.line(screen, WHITE, (0, HEIGHT//2), (WIDTH, HEIGHT//2), 3)
    pygame.draw.rect(screen, WHITE, ((WIDTH - goal_width)//2, 0, goal_width, 10))
    pygame.draw.rect(screen, WHITE, ((WIDTH - goal_width)//2, HEIGHT-10, goal_width, 10))

    # Display scores
    score_text = font.render(f"Player1: {score1}  Player2: {score2}", True, BLUE)
    screen.blit(score_text, (WIDTH//2 - 150, HEIGHT//2 - 20))

    # Display coach instructions
    instr_text = font.render(instruction, True, YELLOW)
    screen.blit(instr_text, (50, 50))

    pygame.display.flip()
    clock.tick(FPS)
