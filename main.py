import pygame
pygame.init()
# pygame.mixer.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 480
FPS = 45
win = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("First Game")

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
DARKGREEN = (0,128,0)

# load images
walkRight = []
walkLeft = []
for index in range(9):
    imageR = pygame.image.load('images/hero_images/R' + str(index+1) + '.png')
    walkRight.append(imageR)
    imageL = pygame.image.load('images/hero_images/L' + str(index+1) + '.png')
    walkLeft.append(imageL)
bg = pygame.image.load('images/bg.jpg')
char = pygame.image.load('images/standing.png')

# Game_variables
clock = pygame.time.Clock()
score = 0

# bulletSound = pygame.mixer.Sound("bullet.wav")
hitSound = pygame.mixer.Sound("hit.wav")
disappearSound = pygame.mixer.Sound("disappear.wav")
music = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)


class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52) # a rectangle

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount//5], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//5], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(win, RED, self.hitbox, 2)
    
    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsan', 100)
        text = font1.render('-5', 1, RED)
        win.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    i = 301
                    pygame.quit


class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class Enemy(object):
    walkRight = []
    walkLeft = []
    for index in range(11): 
        imageR = pygame.image.load('images/enemy_images/R' + str(index+1) + 'E.png')
        walkRight.append(imageR)    
        imageL = pygame.image.load('images/enemy_images/L' + str(index+1) + 'E.png')
        walkLeft.append(imageL)
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 9
        self.visible = True

    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount//5], 
                (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount//5], 
                (self.x, self.y))
                self.walkCount += 1  
            
            # add a health bar 
            pygame.draw.rect(win, RED, (self.hitbox[0], self.hitbox[1]-20, 50,10))
            pygame.draw.rect(win, DARKGREEN, (self.hitbox[0], self.hitbox[1]-20, 50 - (5*(9-self.health)),10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)    
            # pygame.draw.rect(win, RED, self.hitbox, 2)     

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False


def redrawGameWindow():

    win.blit(bg, (0, 0))
    text = font.render('Score: ' + str(score), 1, BLACK)
    win.blit(text, (370, 10)) 
    hero.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)    
    pygame.display.update()


# mainloop
font = pygame.font.SysFont('comicsans', 30, True, True)
hero = Player(300, 410, 64, 64) # create a player 
goblin = Enemy(100, 410, 64, 64, 450)
shootLoop = 0 # set up as a timer 
bullets = []
run = True
while run:
    clock.tick(FPS)

    if goblin.visible:
        if hero.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and hero.hitbox[1] + hero.hitbox[3] > goblin.hitbox[1]:
            if hero.hitbox[0] + hero.hitbox[2] > goblin.hitbox[0] and hero.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                hero.hit()
                score -= 5

    if shootLoop > 0: 
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    for bullet in bullets: # bullet movement
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                pygame.mixer.Sound.play(hitSound)
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel  # vel is directional +/-
        else:
            bullets.pop(bullets.index(bullet))  # delete the edge bullet by index into the bullets list
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        # pygame.mixer.Sound.play(bulletSound)
        if hero.left:
            facing = -1
        elif hero.right:
            facing = 1

        if len(bullets) < 5:
            bullets.append(Projectile(round(hero.x + hero.width // 2),
                                      round(hero.y + hero.height//2), 6, BLACK, facing))

        shootLoop = 1

    if keys[pygame.K_LEFT] and hero.x > hero.vel:
        hero.x -= hero.vel
        hero.left = True
        hero.right = False 
        hero.standing = False   
    elif keys[pygame.K_RIGHT] and hero.x < SCREEN_WIDTH - hero.width - hero.vel:
        hero.x += hero.vel
        hero.right = True
        hero.left = False
        hero.standing = False 
    else:        
        hero.walkCount = 0
        hero.standing = True

    if not hero.isJump:            
        if keys[pygame.K_UP]:
            hero.isJump = True
            hero.right = False
            hero.left = False
            hero.walkCount = 0
            hero.standing = False 
    else:
        if hero.jumpCount >= -10:
            neg = 1
            if hero.jumpCount < 0:
                neg = -1
            hero.y -= (hero.jumpCount ** 2) * 0.5 * neg
            hero.jumpCount -= 1
        else:
            hero.isJump = False
            hero.jumpCount = 10
        
    redrawGameWindow()

pygame.quit()
