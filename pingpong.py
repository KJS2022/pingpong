import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Window setup
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game (Python - Single Player with Game Over)")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game settings
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_RADIUS = 10
PADDLE_SPEED = 7
BALL_SPEED = 6
WIN_SCORE = 5   # First to 5 points wins

# Fonts
SCORE_FONT = pygame.font.SysFont("comicsans", 48)
MENU_FONT = pygame.font.SysFont("comicsans", 36)

# Paddle positions
left_paddle = pygame.Rect(30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball position and velocity
ball = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_RADIUS*2, BALL_RADIUS*2)
ball_vel = [random.choice([-1, 1]) * BALL_SPEED, random.choice([-1, 1]) * BALL_SPEED]

# Scores
score_left = 0
score_right = 0

# AI difficulty
AI_SPEED = 4   # Default (Easy)
AI_REACTION = 20  # Delay factor


def reset_ball():
    """Reset ball to the center with random direction"""
    global ball, ball_vel
    ball.x = WIDTH//2 - BALL_RADIUS
    ball.y = HEIGHT//2 - BALL_RADIUS
    ball_vel = [random.choice([-1, 1]) * BALL_SPEED, random.choice([-1, 1]) * BALL_SPEED]


def draw_window():
    """Draw paddles, ball, middle line, and scores"""
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, WHITE, left_paddle)
    pygame.draw.rect(WIN, WHITE, right_paddle)
    pygame.draw.ellipse(WIN, WHITE, ball)

    # Middle dashed line
    for i in range(0, HEIGHT, 20):
        pygame.draw.rect(WIN, WHITE, (WIDTH//2 - 2, i, 4, 10))

    # Scores
    left_text = SCORE_FONT.render(str(score_left), True, WHITE)
    right_text = SCORE_FONT.render(str(score_right), True, WHITE)
    WIN.blit(left_text, (WIDTH//4 - left_text.get_width()//2, 20))
    WIN.blit(right_text, (WIDTH*3//4 - right_text.get_width()//2, 20))

    pygame.display.update()


def handle_collision():
    """Handle ball collisions with walls and paddles"""
    global ball_vel, score_left, score_right

    # Top and bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_vel[1] *= -1

    # Left paddle
    if ball.colliderect(left_paddle):
        ball_vel[0] *= -1
        offset = (ball.centery - left_paddle.centery) / (PADDLE_HEIGHT//2)
        ball_vel[1] += offset * 2

    # Right paddle (AI)
    if ball.colliderect(right_paddle):
        ball_vel[0] *= -1
        offset = (ball.centery - right_paddle.centery) / (PADDLE_HEIGHT//2)
        ball_vel[1] += offset * 2

    # Scoring
    if ball.left <= 0:
        score_right += 1
        reset_ball()
    elif ball.right >= WIDTH:
        score_left += 1
        reset_ball()


def ai_move():
    """Simple AI to move right paddle"""
    if random.randint(0, AI_REACTION) == 0:  
        if right_paddle.centery < ball.centery:
            right_paddle.y += AI_SPEED
        elif right_paddle.centery > ball.centery:
            right_paddle.y -= AI_SPEED

    # Keep paddle inside window
    if right_paddle.top < 0:
        right_paddle.top = 0
    if right_paddle.bottom > HEIGHT:
        right_paddle.bottom = HEIGHT


def menu_screen():
    """Show start menu with difficulty options"""
    WIN.fill(BLACK)
    title = SCORE_FONT.render("PING PONG GAME", True, WHITE)
    WIN.blit(title, (WIDTH//2 - title.get_width()//2, 150))

    text1 = MENU_FONT.render("Press 1 for Easy", True, WHITE)
    text2 = MENU_FONT.render("Press 2 for Medium", True, WHITE)
    text3 = MENU_FONT.render("Press 3 for Hard", True, WHITE)

    WIN.blit(text1, (WIDTH//2 - text1.get_width()//2, 250))
    WIN.blit(text2, (WIDTH//2 - text2.get_width()//2, 300))
    WIN.blit(text3, (WIDTH//2 - text3.get_width()//2, 350))

    pygame.display.update()

    waiting = True
    global AI_SPEED, AI_REACTION
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Easy
                    AI_SPEED = 4
                    AI_REACTION = 30
                    waiting = False
                elif event.key == pygame.K_2:  # Medium
                    AI_SPEED = 6
                    AI_REACTION = 15
                    waiting = False
                elif event.key == pygame.K_3:  # Hard
                    AI_SPEED = 9
                    AI_REACTION = 5
                    waiting = False


def game_over_screen(winner):
    """Show game over screen"""
    WIN.fill(BLACK)
    text = SCORE_FONT.render(f"{winner} Wins!", True, WHITE)
    info = MENU_FONT.render("Press R to Restart or Q to Quit", True, WHITE)
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
    WIN.blit(info, (WIDTH//2 - info.get_width()//2, HEIGHT//2 + 20))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True   # restart
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def main():
    global score_left, score_right
    clock = pygame.time.Clock()

    while True:  # Allows restart after game over
        score_left, score_right = 0, 0
        menu_screen()  # Show difficulty menu

        run = True
        while run:
            clock.tick(FPS)

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

            # Player controls (W/S)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and left_paddle.top > 0:
                left_paddle.y -= PADDLE_SPEED
            if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
                left_paddle.y += PADDLE_SPEED

            # AI movement
            ai_move()

            # Move ball
            ball.x += ball_vel[0]
            ball.y += ball_vel[1]

            # Collisions
            handle_collision()

            # Draw everything
            draw_window()

            # Check for game over
            if score_left >= WIN_SCORE:
                if not game_over_screen("Player"):
                    run = False
            elif score_right >= WIN_SCORE:
                if not game_over_screen("Computer"):
                    run = False


if __name__ == "__main__":
    main()