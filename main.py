import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pulsa-app")

# Colors
GREEN = (0, 128, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Players
player_size = 50
player_speed = 5
player1_pos = [WIDTH//2 - 100, HEIGHT - 100]
player2_pos = [WIDTH//2 + 100, 100]

# Ball
ball_radius = 20
ball_pos = [WIDTH//2, HEIGHT//2]
ball_speed = [4, -4]

# Scores
score1 = 0
score2 = 0
font = pygame.font.SysFont(None, 36)

# Field
goal_width = 200

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player1_pos[0] > 0:
        player1_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player1_pos[0] < WIDTH - player_size:
        player1_pos[0] += player_speed

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

    # Ball collision with players
    def check_collision(player_pos):
        if (player_pos[0] < ball_pos[0] < player_pos[0] + player_size and
            player_pos[1] < ball_pos[1] < player_pos[1] + player_size):
            return True
        return False

    if check_collision(player1_pos) or check_collision(player2_pos):
        ball_speed[1] *= -1

    # Check goals
    if ball_pos[1] <= 0:  # Player 1 scores
        score1 += 1
        ball_pos = [WIDTH//2, HEIGHT//2]
        ball_speed = [random.choice([-4,4]), 4]
    elif ball_pos[1] >= HEIGHT:  # Player 2 scores
        score2 += 1
        ball_pos = [WIDTH//2, HEIGHT//2]
        ball_speed = [random.choice([-4,4]), -4]

    # Draw everything
    screen.fill(GREEN)
    pygame.draw.rect(screen, WHITE, (player1_pos[0], player1_pos[1], player_size, player_size))
    pygame.draw.rect(screen, RED, (player2_pos[0], player2_pos[1], player_size, player_size))
    pygame.draw.circle(screen, BLACK, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # Draw field lines
    pygame.draw.line(screen, WHITE, (0, HEIGHT//2), (WIDTH, HEIGHT//2), 3)
    pygame.draw.rect(screen, WHITE, ((WIDTH - goal_width)//2, 0, goal_width, 10))
    pygame.draw.rect(screen, WHITE, ((WIDTH - goal_width)//2, HEIGHT-10, goal_width, 10))

    # Draw scores
    score_text = font.render(f"Player1: {score1}  Player2: {score2}", True, BLUE)
    screen.blit(score_text, (WIDTH//2 - 150, HEIGHT//2 - 20))

    pygame.display.flip()
    clock.tick(FPS)
