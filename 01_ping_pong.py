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

