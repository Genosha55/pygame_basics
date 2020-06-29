import pygame
pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 480
win = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("First Game")

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

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.left:
            win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
        else:
            win.blit(char, (self.x,self.y))
        

def redrawGameWindow():

    win.blit(bg, (0,0)) 
    hero.draw(win)    
    pygame.display.update()

# mainloop
hero = Player(300, 410, 64, 64) # create a player 
run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run  = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and hero.x > hero.vel:
        hero.x -= hero.vel
        hero.left = True
        hero.right = False    
    elif keys[pygame.K_RIGHT] and hero.x < SCREEN_WIDTH - hero.width - hero.vel:
        hero.x += hero.vel
        hero.right = True
        hero.left = False
    else:
        hero.right = False
        hero.left = False
        hero.walkCount = 0

    if not hero.isJump:            
        if keys[pygame.K_SPACE]:
            hero.isJump = True
            hero.right = False
            hero.left = False
            hero.walkCount = 0
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