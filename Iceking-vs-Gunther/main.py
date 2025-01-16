import pygame
pygame.init()

# Set the base directory for the images and sound files
base_path = r"C:\Users\User\Downloads\Iceking-vs-Gunther\Iceking-vs-Gunther\pics"

win = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Ice King vs Gunther")

# Load images
walkRight = [pygame.image.load(f"{base_path}\\snowKing_R.png")]
walkLeft = [pygame.image.load(f"{base_path}\\snowKing_L.png")]

bg = pygame.image.load(f"{base_path}\\bg.png")

# Load sounds
hitSound = pygame.mixer.Sound(f"{base_path}\\hit.wav")
bgm = pygame.mixer.music.load(f"{base_path}\\theme.wav")

pygame.mixer.music.play()

Clock = pygame.time.Clock()

# Maximum health bar width
MAX_HEALTH_WIDTH = 200

class player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 10
        self.isjump = False
        self.jumpheight = 10
        self.left = False
        self.right = True  # Default to facing right
        self.hitbox = (self.x + 10, self.y + 5, 80, 80)
        self.health = 200

    def draw(self, win):
        if self.health > 0:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            elif self.left:
                win.blit(walkLeft[0], (self.x, self.y))

            self.hitbox = (self.x + 10, self.y + 5, 80, 80)
        else:
            text = font.render('Gunther Wins', True, (255, 255, 255), (0, 0, 100))
            win.blit(text, (180, 200))

    def hit(self):
        if self.health > 0:
            self.health -= 5
        else:
            print("Ice King died")


class weapons():
    def __init__(self, x, y, width, height, facing):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.facing = facing
        self.vel = 8 * facing
        self.hitbox = (self.x, self.y, 40, 40)

    def draw(self, win):
        win.blit(pygame.image.load(f"{base_path}\\snowball.png"), (self.x, self.y))
        self.hitbox = (self.x, self.y, 40, 40)


class enemy():
    walkRightS = pygame.image.load(f"{base_path}\\Gunther_R.png")
    walkLeftS = pygame.image.load(f"{base_path}\\Gunther_L.png")

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.speed = 8
        self.hitbox = (self.x + 10, self.y + 5, 80, 80)
        self.health = 200

    def draw(self, win):
        self.move()

        if self.health > 0:
            if self.speed > 0:
                win.blit(self.walkRightS, (self.x, self.y))
            else:
                win.blit(self.walkLeftS, (self.x, self.y))

            self.hitbox = (self.x + 10, self.y + 5, 80, 80)
        else:
            self.speed = 0
            text = font.render('Ice King Wins', True, (255, 255, 255), (0, 0, 100))
            win.blit(text, (180, 200))

    def move(self):
        if self.speed > 0:
            if self.x + self.speed < self.path[1]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1
        else:
            if self.x - self.speed > self.path[0]:
                self.x += self.speed
            else:
                self.speed = self.speed * -1

    def hit(self):
        if self.health > 0:
            self.health -= 10
        else:
            print('Gunther died')


run = True
paused = False

# Pause and restart button positions and dimensions
pause_button_rect = pygame.Rect(300, 10, 100, 30)
restart_button_rect = pygame.Rect(290, 50, 120, 30)

def draw_buttons():
    # Draw the pause button
    pygame.draw.rect(win, (200, 0, 0), pause_button_rect)
    pause_text = font_small.render("Pause", True, (255, 255, 255))
    win.blit(pause_text, (pause_button_rect.x + 10, pause_button_rect.y -7))

    # Draw the restart button
    pygame.draw.rect(win, (0, 200, 0), restart_button_rect)
    restart_text = font_small.render("Restart", True, (255, 255, 255))
    win.blit(restart_text, (restart_button_rect.x + 5, restart_button_rect.y -7))

def redrawgamewindow():
    win.blit(bg, (0, 0))
    iceking.draw(win)
    gunther.draw(win)

    # Ice King's health bar
    pygame.draw.rect(win, (255, 0, 0), (80, 40, MAX_HEALTH_WIDTH, 25))  # Red background
    pygame.draw.rect(win, (255, 255, 0), (80, 40, iceking.health, 25))  # Yellow foreground

    # Gunther's health bar (decreases from right to left)
    pygame.draw.rect(win, (255, 0, 0), (420, 40, MAX_HEALTH_WIDTH, 25))  # Red background
    pygame.draw.rect(win, (255, 255, 0), (420 + (MAX_HEALTH_WIDTH - gunther.health), 40, gunther.health, 25))  # Yellow foreground

    for snowball in snowballs:
        snowball.draw(win)

    draw_buttons()  # Draw the pause and restart buttons

    pygame.display.update()

font = pygame.font.SysFont('comicsans', 60, True)
font_small = pygame.font.SysFont('comicsans', 30, True)

iceking = player(30, 400, 100, 100)
gunther = enemy(100, 400, 100, 100, 600)
snowballs = []
throwSpeed = 0

def reset_game():
    global iceking, gunther, snowballs, throwSpeed, paused
    iceking = player(30, 400, 100, 100)
    gunther = enemy(100, 400, 100, 100, 600)
    snowballs = []
    throwSpeed = 0
    paused = False

while run:
    Clock.tick(25)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause_button_rect.collidepoint(event.pos):
                paused = not paused
            if restart_button_rect.collidepoint(event.pos):
                reset_game()

    if paused:
        pause_text = font.render("Game Paused", True, (255, 255, 255))
        win.blit(pause_text, (180, 200))
        pygame.display.update()
        continue

    if throwSpeed > 0:
        throwSpeed += 1

    if throwSpeed > 3:
        throwSpeed = 0

    if iceking.health > 0 and gunther.health > 0:
        if iceking.hitbox[1] < gunther.hitbox[1] + gunther.hitbox[3] and iceking.hitbox[1] + iceking.hitbox[3] > gunther.hitbox[1]:
            if iceking.hitbox[0] + iceking.hitbox[2] > gunther.hitbox[0] and iceking.hitbox[0] < gunther.hitbox[0] + gunther.hitbox[2]:
                iceking.hit()
                hitSound.play()

    for snowball in snowballs:
        if gunther.health > 0:
            if snowball.hitbox[1] + round(snowball.hitbox[3] / 2) > gunther.hitbox[1] and snowball.hitbox[1] + round(snowball.hitbox[3] / 2) < gunther.hitbox[1] + gunther.hitbox[3]:
                if snowball.hitbox[0] + snowball.hitbox[2] > gunther.hitbox[0] and snowball.hitbox[0] + snowball.hitbox[2] < gunther.hitbox[0] + gunther.hitbox[2]:
                    gunther.hit()
                    hitSound.play()
                    snowballs.pop(snowballs.index(snowball))
        else:
            gunther.speed = 0

        if snowball.x < 699 and snowball.x > 0:
            snowball.x += snowball.vel
        else:
            snowballs.pop(snowballs.index(snowball))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and throwSpeed == 0:
        facing = -1 if iceking.left else 1
        if len(snowballs) < 5:
            snowballs.append(weapons(round(iceking.x + 60), round(iceking.y + 30), 40, 40, facing))
        throwSpeed = 1

    if keys[pygame.K_LEFT] and iceking.x > iceking.speed:
        iceking.x -= iceking.speed
        iceking.left = True
        iceking.right = False
    elif keys[pygame.K_RIGHT] and iceking.x < 690 - iceking.width - iceking.speed:
        iceking.x += iceking.speed
        iceking.left = False
        iceking.right = True

    if not iceking.isjump:
        if keys[pygame.K_UP]:
            iceking.isjump = True
            iceking.left = False
            iceking.right = False
    else:
        if iceking.jumpheight >= -10:
            neg = 1 if iceking.jumpheight >= 0 else -1
            iceking.y -= (iceking.jumpheight ** 2) * 0.5 * neg
            iceking.jumpheight -= 1
        else:
            iceking.isjump = False
            iceking.jumpheight = 10

    if keys[pygame.K_r]:
        reset_game()

    redrawgamewindow()

pygame.quit()
