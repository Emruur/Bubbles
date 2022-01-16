from types import new_class
import pygame
from pygame import Vector2
from pygame.constants import K_LEFT, K_RIGHT, K_r

import copy
import time

from Mover import Mover
from Shooter import Shooter
from ChainBullet import ChainBullet

BLACK = (10, 10, 30)
GRAY = (80, 80, 100)
WHITE = (230, 230,200)
RED= (200,30,30)
BLUE= (40,40,100)
GREEN= (40,80,60)

WIDTH,HEIGHT= 1000, 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
  
pygame.display.set_caption('Bouncing ball')

pygame.font.init()
GAME_OVER_FONT_1= pygame.font.SysFont("comicsans", 120)
GAME_OVER_FONT_2= pygame.font.SysFont("comicsans", 60)

FPS= 60
clock= pygame.time.Clock()

gravity = Vector2(0,10)

GAME_OVER_EVENT= pygame.USEREVENT + 1
game_over= False

mover5= Mover(140, Vector2( WIDTH/2, 300))

movers= [mover5]

shooter= Shooter(Vector2(0, HEIGHT),25,0.5)
chain_bullets= []

spike_length= 30
spike= pygame.Rect(0,0,WIDTH, spike_length)

def draw():
    screen.fill(GREEN)
    
    for chain in chain_bullets:
        pygame.draw.line(screen,RED,chain.bottom_position,chain.top_position, 3)
    pygame.draw.circle(screen, WHITE, shooter.position, shooter.radius)
    for mover in movers:
        pygame.draw.circle(screen,BLACK,mover.position, mover.mass)

    pygame.draw.rect(screen ,BLUE, spike)

    if game_over:
        game_over_text= GAME_OVER_FONT_1.render("GAME OVER", 1, WHITE)
        screen.blit(game_over_text, (WIDTH/2 - game_over_text.get_width()/2 ,HEIGHT/2 - game_over_text.get_height()/2))

        game_over_text2= GAME_OVER_FONT_2.render("press 'r' to restart", 1, WHITE)
        screen.blit(game_over_text2, (WIDTH/2 - game_over_text2.get_width()/2 ,HEIGHT/2 + 60))

    pygame.display.update()

def update(): 
    update_chains()
    update_balls()

    check_shooter_bounds()
    check_chain_bounds()

    check_game_over()
    check_chain_collisions()

    for mover in movers:
        
        if mover.position.y > HEIGHT- mover.mass:
            mover.velocity.y *= -1
            mover.position.y=  HEIGHT- mover.mass
        elif mover.position.y < mover.mass + spike_length:
            split_spike(mover)
        
        if mover.position.x > WIDTH- mover.mass:
            mover.velocity.x *= -1
            mover.position.x = WIDTH - mover.mass
        elif mover.position.x < mover.mass:
            mover.velocity.x *= -1
            mover.position.x = mover.mass
        
def check_shooter_bounds():
    if shooter.position.x > WIDTH: 
        shooter.position.x= WIDTH
    elif shooter.position.x<0:
        shooter.position.x= 0


def check_chain_bounds():
    for chain in chain_bullets:
        if chain.top_position.y<0 and not chain.anchored:
            chain.anchor(time.time())

def update_balls():
    for mover in movers:
        mover.applyForce(gravity)
        mover.update()
def update_chains():
    global chain_bullets
    chains= []
    for chain in chain_bullets:
        chain.update()
        if not (chain.anchored and time.time() - chain.anchored_in > chain.anchor_duration):
            chains.append(chain)
    chain_bullets= chains

def check_chain_collisions():
    global chain_bullets
    global movers

    removed_chains= []
    removed_movers= []
    added_movers= []
    for chain in chain_bullets:
        for mover in movers:
            distance_vector= mover.position - chain.top_position
            if distance_vector.magnitude()< mover.mass:
                balls=split_ball(mover,chain)
                if balls:
                    added_movers.append(balls[0])
                    added_movers.append(balls[1])
                removed_movers.append(mover)
                removed_chains.append(chain)
            elif abs(chain.top_position.x- mover.position.x)< mover.mass:
                if chain.top_position.y < mover.position.y:
                    balls= split_ball(mover,chain)
                    if balls:
                        added_movers.append(balls[0])
                        added_movers.append(balls[1])
                    removed_movers.append(mover)
                    removed_chains.append(chain)
    
    chain_bullets[:]= [x for x in chain_bullets if not x in removed_chains]
    movers[:]= [x for x in movers if not x in removed_movers]

    for mover in added_movers:
        movers.append(mover)


def check_game_over():
    for mover in movers:
        distance_vector= mover.position - shooter.position
        if distance_vector.magnitude() < shooter.radius + mover.mass:
            pygame.event.post(pygame.event.Event(GAME_OVER_EVENT))

def split_ball(mover,chain):
    if mover.mass < 30:
        return None
    else:
        initial_momentum= mover.momentum()+ chain.momentum()

        mover1= Mover(mover.mass/2, copy.deepcopy(mover.position))
        mover2= Mover(mover.mass/2, copy.deepcopy(mover.position))

        mover1.velocity= initial_momentum/(2* mover1.mass)
        mover2.velocity= initial_momentum/(2* mover2.mass)

        mover1.velocity.x += 1.5
        mover2.velocity.x -= 1.5

        return (mover1, mover2)

def split_spike(mover):
    global new_movers
    removed_movers= []
    added_movers=[]

    if mover.mass < 30:
        removed_movers.append(movers)
    else:
        m1= Mover(mover.mass/2,copy.deepcopy(mover.position),Vector2(1,0))
        m2= Mover(mover.mass/2,copy.deepcopy(mover.position), Vector2(-1,0))

        added_movers.append(m1)        
        added_movers.append(m2)       
        removed_movers.append(mover) 

    movers[:]= [x for x in movers if not x in removed_movers]

    for m in added_movers:
        movers.append(m)

def reset_game():
    shooter.position= Vector2(WIDTH/2, HEIGHT)
    movers.clear()
    chain_bullets.clear()
    m=Mover(140, Vector2( WIDTH/2, 300))
    m.velocity *= 0
    movers.append(m)
    
        

while 1:   
    dt= clock.tick(FPS)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == GAME_OVER_EVENT:
            game_over= True
        if event.type == pygame.KEYDOWN:
            if event.key== pygame.K_SPACE and not game_over:
                if len(chain_bullets)<2:
                    chain_bullets.append(ChainBullet(copy.deepcopy(shooter.position)))

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[K_RIGHT] and not game_over:
        shooter.move_right(dt)
    if keys_pressed[K_LEFT] and not game_over:
        shooter.move_left(dt)
    if game_over and keys_pressed[K_r]:
        reset_game()
        game_over= False
    
    
    update()
    draw()

    

       




