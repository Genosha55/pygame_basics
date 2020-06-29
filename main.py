import pygame
pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 480
FPS = 27
win = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("First Game")

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)

# load images
walkRight = []
walkLeft = []
for index in range(9):
    image = pygame.image.load('images/R' + str(index+1) + '.png')
    walkRight.append(image)
for index in range(9):
    image = pygame.image.load('images/L' + str(index+1) + '.png')
    walkLeft.append(image)
bg = pygame.image.load('images/bg.jpg')
char = pygame.image.load('images/standing.png')

clock = pygame.time.Clock()

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

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))

        
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

def redrawGameWindow():

    win.blit(bg, (0,0)) 
    hero.draw(win)
    for bullet in bullets:
        bullet.draw(win)    
    pygame.display.update()

# mainloop
hero = Player(300, 410, 64, 64) # create a player 
bullets = []
run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run  = False
    
    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel  # vel is directional +/-
        else:
            bullets.pop(bullets.index(bullet)) # delete the edge bullet by index into the bullets list
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if hero.left:
            facing = -1
        elif hero.right:
            facing = 1

        if len(bullets) < 5:
            bullets.append(Projectile(round(hero.x + hero.width // 2), 
            round(hero.y + hero.height//2), 6, BLACK, facing))

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