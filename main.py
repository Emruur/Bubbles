import copy
import time
import os

import pygame
from pygame import Vector2
from pygame.constants import K_LEFT, K_RIGHT, K_r

from ChainBullet import ChainBullet
from LevelModule import Level, LevelManager
from Mover import Mover
from Shooter import Shooter
from ParticleSystem import ParticleManager, BubbleParticles, ChainParticles, ShooterParticles

BLACK = (10, 10, 30)
GRAY = (80, 80, 100)
WHITE = (230, 230,200)
RED= (200,30,30)
BLUE= (40,40,100)
GREEN= (40,80,60)
YELLOW= (250,250,0)

pygame.init()

WIDTH,HEIGHT= 1000, 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
  
pygame.display.set_caption('Bouncing ball')

pygame.font.init()
GAME_OVER_FONT_1= pygame.font.SysFont("comicsans", 120)
GAME_OVER_FONT_2= pygame.font.SysFont("comicsans", 60)

background= pygame.transform.scale(
    pygame.image.load(os.path.join("assets","background2.png")),(WIDTH,HEIGHT))

BALL_IMG= pygame.image.load(
    os.path.join("assets","ball4.png"))
    
SHOOTER_IMG= pygame.image.load(
    os.path.join("assets","shooter.png"))

FPS= 60
clock= pygame.time.Clock()

GAME_OVER_EVENT= pygame.USEREVENT + 1
    #GAME STATE
game_over= False
level_beginning_state= False
finished= False
timeout= False

#Initialize game variables
gravity = Vector2(0,0.25)
movers= []
shooter= Shooter(Vector2(0,0),30,0.6)
chain_bullets= []

spike_length= 50
time_bar_length= 20
spike= pygame.Rect(0,time_bar_length,WIDTH, spike_length)
time_bar= pygame.Rect(0,0,1,time_bar_length)
tb_back= pygame.Rect(0,0,WIDTH,time_bar_length)

level_manager= LevelManager(WIDTH,HEIGHT,shooter.radius)
level= None

particle_manager= ParticleManager()

#Avoid balls from stopping ( avoid automatic lose for the player)
MIN_BOUNCE_SPEED= 7

SPIKE= pygame.transform.scale(
    pygame.image.load(os.path.join("assets","spike2.png")),(spike_length*2, spike_length*2)
)

SHOOTER= pygame.transform.scale(
    pygame.image.load(os.path.join("assets","shooter.png")),(shooter.radius*2, shooter.radius*2)
)

CHAIN_WIDTH= 25
CHAIN=  pygame.transform.scale(
    pygame.image.load(os.path.join("assets","chain.png")),(CHAIN_WIDTH, HEIGHT- time_bar_length)
)

CHAIN_PARTICLE_IMG= pygame.image.load(os.path.join("assets","chain_particle.png"))
    

#load sound effects
pop= pygame.mixer.Sound('assets/pop2.wav')
pop2= pygame.mixer.Sound('assets/pop.wav')
game_over_sound2= pygame.mixer.Sound('assets/game_over2.wav')
chain_sound= pygame.mixer.Sound('assets/chain.wav')
bounce= pygame.mixer.Sound('assets/bounce.wav')
chain_breaking= pygame.mixer.Sound('assets/break.wav')

def draw():
    screen.blit(background,(0,0))

    draw_particles()

    #draw time bar
    pygame.draw.rect(screen,GRAY,tb_back)
    pygame.draw.rect(screen, YELLOW, time_bar)
    
    for chain in chain_bullets:
        screen.blit(CHAIN,(chain.top_position.x- CHAIN_WIDTH/2, chain.top_position.y))

    
    screen.blit(SHOOTER,(shooter.position.x - shooter.radius, shooter.position.y - shooter.radius))

    for mover in movers:
        BALL= pygame.transform.scale(BALL_IMG, (mover.mass*2,mover.mass*2))
            
        screen.blit(BALL, (mover.position.x- mover.mass,mover.position.y- mover.mass))
        #pygame.draw.circle(screen,BLACK,mover.position, mover.mass)

    
    #pygame.draw.rect(screen ,BLUE, spike)
    spike_x_pos= 0
    while(spike_x_pos< WIDTH):
        screen.blit(SPIKE,(spike_x_pos,time_bar_length))
        spike_x_pos+= spike_length*2

    if game_over:
        game_over_text= GAME_OVER_FONT_1.render("GAME OVER", 1, WHITE)
        screen.blit(game_over_text, (WIDTH/2 - game_over_text.get_width()/2 ,HEIGHT/2 - game_over_text.get_height()/2))

        game_over_text2= GAME_OVER_FONT_2.render("press 'r' to restart", 1, WHITE)
        screen.blit(game_over_text2, (WIDTH/2 - game_over_text2.get_width()/2 ,HEIGHT/2 + 60))

        if timeout:
            game_over_text_3= GAME_OVER_FONT_2.render("ran out of time!", 1, WHITE)
            screen.blit(game_over_text_3, (WIDTH/2 - game_over_text_3.get_width()/2 ,HEIGHT/2 + 120))

    if level_beginning_state:
        level_begining_text_1= GAME_OVER_FONT_1.render("LEVEL: "+ str(level_manager.current_level), 1, WHITE)
        screen.blit(level_begining_text_1, (WIDTH/2 - level_begining_text_1.get_width()/2 ,HEIGHT/2 - level_begining_text_1.get_height()/2))

        level_begining_text_2= GAME_OVER_FONT_2.render("press any key to start", 1, WHITE)
        screen.blit(level_begining_text_2, (WIDTH/2 - level_begining_text_2.get_width()/2 ,HEIGHT/2 + 60))
    
    if finished:
        finished_text= GAME_OVER_FONT_2.render("More levels are going to be added ", 1, WHITE)
        screen.blit(finished_text, (WIDTH/2 - finished_text.get_width()/2 ,HEIGHT/2 - finished_text.get_height()/2))

    pygame.display.update()

def draw_particles():
    for particles in particle_manager.particle_systems:
        new_particle_img= None
        if isinstance(particles, BubbleParticles):
            new_particle_img= BALL_IMG.copy()
        elif isinstance(particles, ChainParticles):
            new_particle_img= CHAIN_PARTICLE_IMG.copy()
        
        new_particle_img.set_alpha((1-particles.elapsed_ratio())*100)
        PARTICLE= pygame.transform.scale(new_particle_img,(particles.radius, particles.radius))
        for particle in particles.particles:
            screen.blit(PARTICLE,particle.position)

def update(): 
    global time_bar
    global timeout
    update_chains()
    update_balls()
    update_particles()

    check_shooter_bounds()
    check_chain_bounds()

    check_game_over()
    check_chain_collisions()

    for mover in movers:
        
        if mover.position.y > HEIGHT- mover.mass:
            if(mover.velocity.magnitude() < MIN_BOUNCE_SPEED):#Avoid balls from coming to a full stop
                split_spike(mover)
            mover.velocity.y *= -1
            mover.position.y=  HEIGHT- mover.mass
            bounce.play()
        elif mover.position.y < mover.mass + spike_length+ time_bar_length:
            split_spike(mover)
        
        if mover.position.x > WIDTH- mover.mass:
            mover.velocity.x *= -1
            mover.position.x = WIDTH - mover.mass
        elif mover.position.x < mover.mass:
            mover.velocity.x *= -1
            mover.position.x = mover.mass

        

    #update time bar
    if not game_over:
        time_bar.width= WIDTH* level.elapsed()

    if level.lost() and not game_over:
        pygame.mixer.Sound.play(game_over_sound2)
        timeout= True
        pygame.event.post(pygame.event.Event(GAME_OVER_EVENT))
        

        
def check_shooter_bounds():
    if shooter.position.x > WIDTH: 
        shooter.position.x= WIDTH
    elif shooter.position.x<0:
        shooter.position.x= 0


def check_chain_bounds():
    for chain in chain_bullets:
        if chain.top_position.y<0 and not chain.anchored:
            chain.anchor(time.time())
            chain_sound.stop()
        


def update_balls():
    for mover in movers:
        mover.applyForce(gravity* mover.mass)
        mover.update()
def update_chains():
    global chain_bullets
    chains= []
    for chain in chain_bullets:
        chain.update()
        if not (chain.anchored and time.time() - chain.anchored_in > chain.anchor_duration):
            chains.append(chain)
        else:
            #add chain particles
            chain_particle_system= ChainParticles(chain.bottom_position,HEIGHT, HEIGHT)
            particle_manager.add_particle_system(chain_particle_system)
            chain_breaking.play()
    chain_bullets= chains
def update_particles():
    for particles in particle_manager.particle_systems:
        if particles.disappeared():
            particle_manager.particle_systems.remove(particles)
        else:
            particles.update_system(gravity*1.7)

def check_chain_collisions():
    global chain_bullets
    global movers

    removed_chains= []
    removed_movers= []
    added_movers= []
    for chain in chain_bullets:
        for mover in movers:
            distance_vector= mover.position - chain.top_position
            if distance_vector.magnitude()< mover.mass + chain.width:
                balls=split_ball(mover,chain)
                if balls:
                    pygame.mixer.Sound.play(pop)
                    added_movers.append(balls[0])
                    added_movers.append(balls[1])
                else:
                    #add particles 
                    particles= BubbleParticles(1.5,mover.position, mover.momentum()+ chain.momentum())
                    particle_manager.add_particle_system(particles)
                    pygame.mixer.Sound.play(pop2)
                removed_movers.append(mover)
                removed_chains.append(chain)
                chain_sound.stop()
                
            elif abs(chain.top_position.x- mover.position.x)< mover.mass + chain.width:
                if chain.top_position.y < mover.position.y:
                    balls= split_ball(mover,chain)
                    if balls:
                        pygame.mixer.Sound.play(pop)
                        added_movers.append(balls[0])
                        added_movers.append(balls[1])
                    else:
                        #add particles 
                        particles= BubbleParticles(1.5,mover.position,mover.momentum()+ chain.momentum())
                        particle_manager.add_particle_system(particles)
                        pygame.mixer.Sound.play(pop2)
                    removed_movers.append(mover)
                    removed_chains.append(chain)
                    chain_sound.stop()

    
    chain_bullets[:]= [x for x in chain_bullets if not x in removed_chains]
    movers[:]= [x for x in movers if not x in removed_movers]

    for mover in added_movers:
        movers.append(mover)


def check_game_over():
    for mover in movers:
        distance_vector= mover.position - shooter.position
        if distance_vector.magnitude() < shooter.radius + mover.mass and not game_over:
            pygame.mixer.Sound.play(game_over_sound2)
            
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
    movers.remove(mover)
    pop2.play()
    particles= BubbleParticles(2,mover.position,mover.momentum())
    particle_manager.add_particle_system(particles)

def init_game():
    global level
    global level_beginning_state
    global time_bar
    #level_manager.reset()
    level= level_manager.load_level()
    shooter.position= copy.deepcopy(level.shooter_location)

    chain_bullets.clear()
    movers.clear()
    for mover in level.movers:
        movers.append(copy.deepcopy(mover))

    time_bar.width= 1

    level_beginning_state= True

def load_next_level():
    global finished
    global level_beginning_state
    global level
    global time_bar
    
    level= level_manager.load_level()
    time_bar.width= 1

    if level:
        shooter.position= copy.deepcopy(level.shooter_location)
        chain_bullets.clear()
        movers.clear()

        for mover in level.movers:
            movers.append(copy.deepcopy(mover))

        level_beginning_state= True
    else:
        finished= True


init_game()
while 1:   
    dt= clock.tick(FPS)
    if len(movers)<= 0 and not game_over:
        load_next_level()
        
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == GAME_OVER_EVENT:
            chain_sound.stop()
            game_over= True
        if event.type == pygame.KEYDOWN:
            if not level_beginning_state:
                if event.key== pygame.K_SPACE and not game_over:
                    if len(chain_bullets)<2:
                        chain_bullets.append(ChainBullet(copy.deepcopy(shooter.position)))
                        chain_sound.play()
            else:
                level.start()
                level_beginning_state= False


    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[K_RIGHT] and not game_over and not level_beginning_state:
        shooter.move_right(dt)
    if keys_pressed[K_LEFT] and not game_over and not level_beginning_state:
        shooter.move_left(dt)
    if game_over and keys_pressed[K_r]:
        init_game()
        game_over= False
        timeout= False
    
    if not level_beginning_state:
        if not game_over:
            update()
    else:
        update_particles()

    draw()

    

       




