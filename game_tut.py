import pygame
import os

pygame.font.init()
pygame.mixer.init()

HEALTH_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',100)

WIDTH , HEIGHT = 1300,700 #900,500
WIN = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption('Space Wars!!!')

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BORDER = pygame.Rect(645, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/karve.mp3')
BULLET_FIRE_SOUND_1 = pygame.mixer.Sound('Assets/hato.mp3')
BULLET_FIRE_SOUND_2 = pygame.mixer.Sound('Assets/systemm.mp3')
WINNER_SOUND=pygame.mixer.Sound('Assets/karve.mp3')
BG=pygame.mixer.Sound('Assets/badal_1.mp3')

BULLET_FIRE_SOUND_1.set_volume(0.2)
BULLET_FIRE_SOUND_2.set_volume(0.2)
BG.set_volume(0.3)

SHIP_WIDTH = 80
SHIP_HEIGHT = 65
FPS = 60
VEL = 5
BULLETS_VEL = 7
MAX_BULLETS = 6

RED_HIT = pygame.USEREVENT +1
YELLOW_HIT = pygame.USEREVENT +2

SPACE_IMG = pygame.image.load('Assets/space.png')
SPACE = pygame.transform.scale(SPACE_IMG,(WIDTH,HEIGHT))

YELLOW_SHIP = pygame.image.load('Assets/spaceship_yellow.png')
Y_SHIP = pygame.transform.rotate(
         pygame.transform.scale(
            YELLOW_SHIP,(SHIP_WIDTH,SHIP_HEIGHT)), 270)

RED_SHIP = pygame.image.load('Assets/spaceship_red.png')
R_SHIP = pygame.transform.rotate(
         pygame.transform.scale(
            RED_SHIP,(SHIP_WIDTH,SHIP_HEIGHT)), 90)

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, winner_text):
    
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    
    red_health_text = HEALTH_FONT.render('Health: ' + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render('Health: ' + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text,(10,10))
    WIN.blit(yellow_health_text,(WIDTH-200,10))
    
    WIN.blit(R_SHIP,(red.x, red.y))
    WIN.blit(Y_SHIP,(yellow.x, yellow.y))
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
        
    pygame.display.update()

def draw_winner(text):
    BG.stop()
    win_text = WINNER_FONT.render(text,1, WHITE)
    WINNER_SOUND.play()
    WIN.blit(win_text,(WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - win_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)

def red_movement(keys_pressed,red):
    
    if keys_pressed[pygame.K_a] and red.x > 5 : #--i.e for left movement---
        red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x < 575 : #--i.e for right movement---
        red.x += VEL    
    if keys_pressed[pygame.K_w] and red.y > 5 : #--i.e for up movement---
        red.y -= VEL
    if keys_pressed[pygame.K_s] and red.y < 615 : #--i.e for down movement---
        red.y += VEL 

def yellow_movement(keys_pressed,yellow):
    
    if keys_pressed[pygame.K_LEFT] and yellow.x-VEL > 655 : #--i.e for left movement---
        yellow.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and yellow.x-VEL < 1225 : #--i.e for right movement---
        yellow.x += VEL    
    if keys_pressed[pygame.K_UP] and yellow.y-VEL > 0 : #--i.e for up movement---
        yellow.y -= VEL
    if keys_pressed[pygame.K_DOWN] and yellow.y-VEL < 610 : #--i.e for down movement---
        yellow.y += VEL 

def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    
    for bullet in red_bullets:
        bullet.x +=BULLETS_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)
        
    for bullet in yellow_bullets:
        bullet.x -=BULLETS_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)

def main():
    
    red = pygame.Rect(100,150,SHIP_WIDTH,SHIP_HEIGHT)
    yellow = pygame.Rect(1100,300,SHIP_WIDTH,SHIP_HEIGHT)
    
    red_bullets = []
    yellow_bullets = []
    
    red_health=10
    yellow_health=10
    
    BG.play(-1)
    clock = pygame.time.Clock()
    run = True
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                pygame.quit() 
                   
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height//2 -2,10,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND_1.play()
                    
                if event.key == pygame.K_RCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2 -2,10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND_2.play()
            
            if event.type == RED_HIT:
                red_health -=1
                BULLET_HIT_SOUND.play()
                
            if event.type == YELLOW_HIT:
                yellow_health -=1
                BULLET_HIT_SOUND.play()
        
        winner_text=''
        if red_health <=0:
            winner_text='Yellow Wins!!!'
        if yellow_health <=0:
            winner_text='    Red Wins!!!'
        if winner_text!='':
            draw_winner(winner_text)
            break
               
        keys_pressed = pygame.key.get_pressed()
        red_movement(keys_pressed, red)
        yellow_movement(keys_pressed, yellow)
        
        draw_window(red, yellow,red_bullets,yellow_bullets,red_health,yellow_health,winner_text)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
    
    main()

if __name__ == "__main__":
    main()