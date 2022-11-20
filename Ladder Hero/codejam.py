from cgitb import text
from platform import platform
from sre_constants import JUMP
import random
from tkinter import CENTER
import pygame
pygame.init()
screen_width = 1500
screen_height = 800
win = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Ladder Hero")
pygame.mixer.init()
pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1)
left = True
right = False 

walk_right = pygame.image.load('jerryright.png')
walk_left = pygame.image.load('jerryleft.png')

image_enemy_right = pygame.image.load('tomright.png')
image_enemy_left = pygame.image.load('tomleft.png')

background = pygame.image.load('background.png')

image_platform = pygame.image.load('platform.png')

image_ladder = pygame.image.load('ladder.png')

cheese = pygame.image.load('cheese.png')

class Player():
    def __init__(self, x , y, width, height):
        self.x = x
        self.y = y 
        self.width = width
        self.height = height
        self.isJump = False
        self.jumpCount = 10
        self.vel = 10
        self.hitbox = (self.x, self.y,self.x+width,self.y+height)
        self.ladder = False
        self.up = 30
        self.onPlatform = False

    def draw(self,win):
        self.hitbox = (self.x, self.y,self.width,self.height)
        if right:
            win.blit(walk_right, (self.x,self.y))
        elif left:
            win.blit(walk_left, (self.x,self.y))
    
    def corners(self):
        
        four_corners = [self.x,self.y,self.x+self.width,self.y+self.height]
        return four_corners
    
    def center(self):
        center = (self.x+0.5*self.width,self.y+self.height)
        return center
    def go_down(self,distance):
        self.y += distance

class Ennemies():
    def __init__(self,x,y,width,height,end,vel):
        self.x = x
        self.y = y 
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = vel

    def movement_enemy(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel 
            else:
                self.vel = self.vel*-1
        else:
            if self.x + self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1  

    def draw(self,win):
        if self.vel > 0:
            win.blit(image_enemy_right, (self.x,self.y,))
        else:
            win.blit(image_enemy_left, (self.x,self.y,))

    def go_down(self,distance):
        self.y += distance

            

class Platform():
    def __init__(self, x , y, width, height):
        self.x = x
        self.y = y 
        self.width = width
        self.height = 15
        self.hitbox =(self.x,self.y,self.width,self.height)
        self.center = self.x+0.5*self.width

    def draw_platform(self,win):
        
        self.hitbox =(self.x,self.y,self.width,self.height)
        win.blit(image_platform, (self.x,self.y-50))
        
    def on_platform(self, center):
        if center[1] < self.y + self.height and center[0] < self.x +self.width and center[0] > self.x and center[1] > self.y - 5:
            man.onPlatform = True 
    def go_down(self, distance):
        self.y += distance

       


class ladder():
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y 
        self.width = width
        self.height = height
        self.hitbox = (self.x,self.y,self.width,self.height)
        self.center = self.x+0.5*self.width

    def draw_ladder(self,win):
        
        self.hitbox = (self.x, self.y,self.width,self.height)
        win.blit(image_ladder, (self.x-33,self.y))

    def isInLadder(self,center):
        if center[0] < self.x + self.width and self.x < center[0]:
            if center[1] <= self.y + self.height+30 and self.y <= center[1]:
                man.ladder = True
    def go_down(self,distance):
        self.y += distance

def get_distance(man):
    if man.y < 400:
        return 400 - man.y
    return 0

def generate_platforms(ladders,platforms):
    x = ladders[-1].center
    y = ladders[-1].y
    widthL = ladders[-1].width
    widthP = platforms[-1].width
    if 0 < x <= widthL:
        newX = random.randint(widthL, widthL+widthP)
        platforms.append(Platform(newX,y,600,30))
      
    elif widthL < x <= 1920-widthL:
        newX = random.randint(widthL, widthL+widthP)
        platforms.append(Platform(newX,y,600,30))
        
    elif 1920-widthL < x < 1920:
        newX = random.randint(widthL, 1920-widthP)
        platforms.append(Platform(newX,y,600,30))
    

enemies = []
def generate_enemies(platforms,ennemies):
    x = platforms[-1].x 
    y = platforms[-1].y
    width = platforms[-1].width
    chance = random.randint(0,1)
    chance2 = random.randint(0,1)
    vel1 = random.randint(4,8)
    vel2 = random.randint(1,3)
    if chance == 0:
        the_ennemies.append(Ennemies(x+25,y-75,75,75,x+width-100,vel1))
    if chance2 == 0:
        the_ennemies.append(Ennemies(x-25,y-75,75,75,x+width-100,vel2))




def generate_ladders(ladders,platforms,ennemies):
    x = platforms[-1].x
    width = platforms[-1].width
    y = platforms[-1].y
    if ladders[-1].y > 50:
        x = random.randint(x,x+width-50)
        ladders.append(ladder(x,platforms[-1].y-200,50,200))
        generate_platforms(ladders,platforms)
        generate_enemies(platforms,ennemies)
        
def write_score(score):
    font = pygame.font.SysFont('comicsans', 25, True)
    text = font.render("score: "+str(score),True , (0,0,0))
    win.blit(text, (1300,10))
        
    

    
man = Player(500,500,50,50)

ladder1 = ladder(500,500,50,200)

ladders = [ladder1]

platform1 = Platform(490,490,600,30)

platforms = [platform1]

the_ennemies = []

run = True    

def redraw():
    run = True
    win.blit(background, (0,0))
    
    
    collision = False
    for enemy in the_ennemies:
        if (man.y >= enemy.y and man.y <= enemy.y + enemy.height) or (man.y + man.height >= enemy.y and man.y + man.height <= enemy.y + enemy.height):
            if (man.x >= enemy.x  and man.x <= enemy.x + enemy.width) or (man.x + man.width >= enemy.x and man.x + man.width <= enemy.x + enemy.width):
                collision = True

  
    for enemy in the_ennemies:       
        enemy.movement_enemy()
   
    for villain in the_ennemies:
        villain.draw(win)

    
    for lads in ladders:
        lads.draw_ladder(win)
    
    for plat in platforms:
        plat.draw_platform(win)

    man.draw(win)
    score = len(platforms) - 4
    write_score(score)
    if collision:
        font = pygame.font.SysFont('comicsans', 50, True)
        text = font.render('skill issue',True , (200,0,0))
        win.blit(text, (750,400))
        collision = False
        run = False
    win.blit(cheese, (730,0))

    pygame.display.update()

    return run

while run:
   
    pygame.time.delay(50)
    generate_ladders(ladders,platforms,the_ennemies)
    distance = get_distance(man) 
    if distance != 0:
        for lads in ladders:
            lads.go_down(distance)
        for plats in platforms:
            plats.go_down(distance)
        man.go_down(distance)
        for enemy in the_ennemies:
            enemy.go_down(distance)
        distance = 0
    
    keys = pygame.key.get_pressed()
    man.onPlatform = False
    man.ladder = False

    for lads in ladders:
        lads.isInLadder(man.center())
    for plats in platforms:
        plats.on_platform(man.center())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    if keys[pygame.K_RIGHT] and man.x < screen_width-man.width:
        man.x += man.vel
        left = False
        right = True
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        left = True
        right = False

    if not man.isJump:
        if keys[pygame.K_SPACE]:
            man.isJump = True
    else:
        if man.jumpCount >= -10:
            
           neg = 1
           if man.jumpCount <0:
               neg = 0
           man.y -= neg*(man.jumpCount**2)*0.7
           man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    if man.ladder:
        if keys[pygame.K_UP] and man.y > man.vel:
            man.y -= man.up

    if man.ladder and man.isJump:
        man.isJump = False

    for i in range(15):
        if man.y < screen_height - man.height and man.ladder == False and man.onPlatform == False:
            man.y += 1
    run = redraw()
    center = man.center()
    if center[1] >= screen_height:
        run = False
    if run == False:
        font = pygame.font.SysFont('comicsans', 50 , True)
        text = font.render('GAME OVER',True , (200,0,0))
        win.blit(text, (400,400))
        pygame.display.update()
        pygame.time.delay(2000)

pygame.quit()







