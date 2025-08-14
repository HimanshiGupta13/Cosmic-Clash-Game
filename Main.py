import pygame
import random
import time
pygame.font.init()
pygame.mixer.init()

WIDHT=900
HEIGHT=600

WIN=pygame.display.set_mode((WIDHT,HEIGHT))
pygame.display.set_caption("Galaxy Fighter")
FONT=pygame.font.SysFont("comicsans",20,bold="True")
Time_FONT=pygame.font.SysFont("comicsans",20)
WINNER_FONT=pygame.font.SysFont("comicsans",70,bold="True")
BG=pygame.transform.scale(pygame.image.load("space.png"),(WIDHT,HEIGHT))
AREA_PLAYER1=WIDHT//2
AREA_PLAYER2=WIDHT//2

PLAYER1_WIDTH=AREA_PLAYER1//2
PLAYER1_HEIGHT=HEIGHT//2
PLAYER2_WIDTH=AREA_PLAYER1+AREA_PLAYER2//2
PLAYER2_HEIGHT=HEIGHT//2
SPACESHIP_WIDTH,SPACESHIP_HEIGHT=35,35
VEL=3

BORDER=pygame.Rect(WIDHT//2-2.5,0,5,HEIGHT)
BULLET_FIRE_SOUND=pygame.mixer.Sound("Bullet_Hit_Sound.mp3")
BULLET_HIT_SOUND=pygame.mixer.Sound("Bullet_Hit_Sound.mp3")

BULLET_VEL=7
MAX_BULLETS=3

YELLOW_HIT=pygame.USEREVENT +1
RED_HIT=pygame.USEREVENT +2

player1=pygame.transform.scale(pygame.image.load("spaceship_red.png"),(SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
player2=pygame.transform.scale(pygame.image.load("spaceship_yellow.png"),(SPACESHIP_WIDTH,SPACESHIP_HEIGHT))

def handle_movement_red(keys_pressed,red):
    if keys_pressed[pygame.K_UP] and red.y -VEL >0:  
            red.y-=VEL
    elif keys_pressed[pygame.K_DOWN] and red.y +VEL+SPACESHIP_WIDTH<HEIGHT:
            red.y+=VEL
    elif keys_pressed[pygame.K_LEFT] and red.x -VEL >0:
            red.x-=VEL
    elif keys_pressed[pygame.K_RIGHT] and red.x +SPACESHIP_HEIGHT+5+ VEL < BORDER.x:
            red.x+=VEL

def handle_movement_yellow(keys_pressed,yellow):
    if keys_pressed[pygame.K_u] and yellow.y -VEL >0:  
            yellow.y-=VEL
    elif keys_pressed[pygame.K_d] and yellow.y+ SPACESHIP_WIDTH+VEL <HEIGHT:
            yellow.y+=VEL
    elif keys_pressed[pygame.K_l] and yellow.x + VEL >BORDER.x+20:
            yellow.x-=VEL
    elif keys_pressed[pygame.K_r] and yellow.x +VEL+35 <WIDHT:
            yellow.x+=VEL

def handle_bullets(red_bullets,yellow_bullets,red,yellow):
    for bullet in red_bullets:
        bullet.x+=BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x >WIDHT:
             red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x-=BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x<0:
            yellow_bullets.remove(bullet)

def draw(elapsed_time,red,yellow,red_bullets,yellow_bullets,RED_health,YELLOW_health):

    WIN.blit(BG,(0,0))

    pygame.draw.rect(WIN,"black",BORDER)

    time_text=Time_FONT.render(f"Time: {round(elapsed_time)}s",1,"white")
    WIN.blit(time_text,(5,5))

    WIN.blit(pygame.transform.rotate(player1,90),(red.x,red.y))
    WIN.blit(pygame.transform.rotate(player2,-90),(yellow.x,yellow.y))

    health_display1=FONT.render(f"Health: {RED_health}",1,"white")
    WIN.blit(health_display1,(10,health_display1.get_height()+20))
    health_display2=FONT.render(f"Health: {YELLOW_health}",1,"white")
    WIN.blit(health_display2,(WIDHT-health_display2.get_width()-20,health_display2.get_height()+20))

    for bullets in red_bullets:
         pygame.draw.rect(WIN,"red",bullets)
    for bullets in yellow_bullets:
         pygame.draw.rect(WIN,"yellow",bullets)

    pygame.display.update()

def draw_winner(text):
    results=WINNER_FONT.render(text,1,"white")
    WIN.blit(results,(WIDHT/2-results.get_width()/2,HEIGHT/2-results.get_height()/2))
    pygame.display.update()
    pygame.time.delay(6000)


def main():

    red=pygame.Rect(PLAYER1_WIDTH,PLAYER1_HEIGHT,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow=pygame.Rect(PLAYER2_WIDTH,PLAYER2_HEIGHT,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    
    red_bullets=[]
    yellow_bullets=[]

    RED_health=5
    YELLOW_health=5

    run=True
    clock=pygame.time.Clock()
    start_time=time.time()
    elapsed_time=0

    while run :

        clock.tick(60)
        elapsed_time=time.time()-start_time
        for event in pygame.event.get():
            if event.type== pygame.QUIT :
                run=False
                break
            
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LCTRL and len(red_bullets)<MAX_BULLETS:
                            #fire
                    bullet=pygame.Rect(red.x+red.width,red.y+red.height//2,10,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key==pygame.K_RCTRL and len(yellow_bullets)<MAX_BULLETS:
                    bullet=pygame.Rect(yellow.x,yellow.y+yellow.height//2,10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type==RED_HIT:
                RED_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type ==YELLOW_HIT:
                YELLOW_health -= 1
                BULLET_HIT_SOUND.play()
        winner_text=""
        if RED_health<=0:
            winner_text="Yellow Wins!" 
        if YELLOW_health<=0:
            winner_text="Red Wins!"
        if winner_text!="":
            draw_winner(winner_text)
            break
        keys_pressed=pygame.key.get_pressed()
        handle_movement_red(keys_pressed,red)
        handle_movement_yellow(keys_pressed,yellow)
        handle_bullets(red_bullets,yellow_bullets,red,yellow)
        draw(elapsed_time,red,yellow,red_bullets,yellow_bullets,RED_health,YELLOW_health)
    pygame.quit()

if __name__=="__main__":
    main()