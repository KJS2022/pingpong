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

racket1 = None
racket2 = None
ball = None
font.init()
score_font = font.Font(None, 56)
hint_font = font.Font(None, 28)
score1, score2 = 0,0
paused = False 

class GameSprite(sprite.Sprite):
    def __init__(self,surf,x,y,speed=0):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_rect(topleft=(x,y))
        self.speed = speed

    def reset(self):
        window.blit(self.image, self.rect.topleft)

class Player(GameSprite):
    def clamp(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > win_height:
            self.rect.bottom = win_height

    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w]:
            self.rect.y -= self.speed
        if keys[K_s]:
            self.rect.y += self.speed
        self.clamp()


    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP]:
            self.rect.y -= self.speed
        if keys[k_DOWN]:
            self.rect.y += self.speed
        self.clamp()
def draw_court():
    window.fill(BACK)
    draw.rect(window, LINES, Rect(8, 8, win_width - 16, win_height - 16), 4)
    dash_h = 18
    gap_h = 14
    x = win_width // 2
    y = 8
    while y < win_height - 8:
        draw.line(window, LINES, (x, y), (x, min(y + dash_h, win_height - 8)), 4)
        y += dash_h + gap_h

def draw_ui():
    score_text = score_font.render(f"{score1} : {score2}", True, LINES)
    window.blit(score_text,(win_width//2 - score_text.get_width()//2,16))

    if winner is not None:
        win_text = hint_font.render(f"Player {winner} wins! Press R to reset", True, LINES)
        window.blit(win_text,(win_width//2 - win_text.get_width()//2,60))






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
                racket1.rect.centery = win_height // 2
                racket2.rect.centery = win_height // 2
                ball.center_serve(direction=1)

    draw_court()
    draw_ui()
    display.update()
    clock.tick(FPS)

quit()
    