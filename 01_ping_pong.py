from pygame import *

init()
win_width, win_height = 800,500
window = display.set_mode((win_width,win_height))
display.set_caption("Ping Pong")

clock = time.Clock()
FPS = 60

BACK = (16,120,16)
LINES = (240,240,240)
PADD = (240,240,240)
BALLC = (240,240,240)

PAD_W, PAD_H = 14, 120
BALL_R = 10
PAD_GAP = 30
BASE_SPEED_PADDLE = 6
BALL_SPEED_X = 4
BALL_SPEED_Y = 3

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                game = False
            if e.key == K_p:
                paused = not paused
            if e.key == K_r:
                score1 = score2 = 0
                winner = None
                racket1.rect.centery = win_height //2
                racket2.rect.centery = win_height //2
                ball.center_serve(direction=1)
    