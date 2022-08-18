from cmath import rect
from turtle import color, left, right
import pygame
from pygame import mixer

pygame.init()
mixer.init()

win = pygame.display.set_mode((1080, 1080))
pygame.display.set_caption("JojoFunkie")

lknife = pygame.image.load('lknife.png')
rknife = pygame.image.load('rknife.png')

box = pygame.Rect(700, 566, 100, 100)

walkRight = [pygame.image.load('diorwalk1.png'), pygame.image.load('diorwalk2.png'), pygame.image.load('diorwalk3.png')]
walkLeft = [pygame.image.load('diolwalk1.png'), pygame.image.load('diolwalk2.png'), pygame.image.load('diolwalk3.png')]
char = pygame.image.load('diostanding.png')
bg = pygame.image.load('background.jpg')

knifesound = mixer.Sound('knife.wav')

clock = pygame.time.Clock()

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 15
        self.isJump = False
        self.jumpCount = 11
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x, self.y, 70, 100)                                     #Hitbox

    def draw(self,win): 
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//9 ], (self.x, self.y))   
                self.walkCount += 1
                self.hitbox = (self.x, self.y, 70, 100)                                   #Hitbox
                pygame.draw.rect(win, (255, 0, 255), self.hitbox, 2)
            elif self.right: 
                win.blit(walkRight[self.walkCount//9], (self.x, self.y))     
                self.walkCount += 1
                self.hitbox = (self.x, self.y, 70, 100)                                   #Hitbox
                pygame.draw.rect(win, (255, 0, 255), self.hitbox, 2)
        else: 
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:    
                win.blit(walkLeft[0], (self.x, self.y))
            self.hitbox = (self.x, self.y, 70, 100)                                   #Hitbox
            pygame.draw.rect(win, (255, 0, 255), self.hitbox, 2)                      #Hitbox
        
        if box.colliderect(self.hitbox):
           if dio.x < 750: 
            dio.vel = 0
            if dio.left == True:
                dio.vel = 15
           if dio.x > 750:
            dio.vel = 0
            if dio.right == True:
                dio.vel = 15    
           if dio.y < 566:
            self.y -= 100          

class knife(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 30 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius) 
        self.couteau = (self.x, self.y, 50, 15)                                 
        pygame.draw.rect(win, (128,128,128), self.couteau) 

def redrawGameWindow():
    win.blit(bg, (0, 0,))
    dio.draw(win)
    for bullet in bullets:
        bullet.draw(win)   
    pygame.display.update()
    
dio = player(1000, 566, 64, 64)
bullets = []
run = True
while run:

    pygame.draw.rect(win, (255, 0, 0), box)
    pygame.display.flip()

    clock.tick(60)

    for event in pygame.event.get() :
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < 1600 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))            

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        
        if dio.left:
            facing = -1
        else:
            facing = 1    
        if len(bullets) < 1:
            bullets.append(knife(round(dio.x + dio.width //2), round(dio.y + dio.height//2), 1, (0, 0, 0), facing))
            knifesound.play()

    if keys[pygame.K_LEFT] and dio.x > dio.vel:
        dio.x -= dio.vel
        dio.left = True
        dio.right = False
        dio.standing = False
    elif keys[pygame.K_RIGHT] and dio.x < 1080 - dio.width - dio.vel:
        dio.x += dio.vel
        dio.right = True
        dio.left = False 
        dio.standing = False

    else:
        dio.standing = True
        dio.walkCount = 0    

    if not(dio.isJump):
        if keys[pygame.K_UP]:
            dio.isJump = True
            dio.right = False
            dio.left = False
            dio.walkCount = 0
    else:
        if dio.jumpCount >= -11:
            neg = 1
            dio.vel = 15
            if dio.jumpCount < 0:
                neg = -1
            dio.y -= (dio.jumpCount ** 2) * 0.5 * neg
            dio.jumpCount -= 1
        else:
            dio.isJump = False
            dio.jumpCount = 11   
            dio.vel = 15 
        
    redrawGameWindow()
    
pygame.quit()                                    