from pygame import Vector2
import time
from Mover import Mover
from random import randint
from copy import deepcopy

class ParticleSystem:  #Particle system interface
    def start(self):
        self.init_time= time.time()

    def update_system(self,g):
        for particle in self.particles:
            particle.applyForce(g*particle.mass)
            particle.update()
    def elapsed_ratio(self):
        return (time.time()- self.init_time) / self.duration 

    def disappeared(self):
        return self.elapsed_ratio() > self.threshold


class ParticleManager:

    def __init__(self) ->None:
        self.particle_systems= []

    def add_particle_system(self,particles):
        self.particle_systems.append(particles)

    

class BubbleParticles(ParticleSystem):
    def __init__(self, duration, position, momentum) -> None:
        super().__init__()
        self.particles= []
        self.duration= duration
        self.threshold= 0.7
        self.radius= 10

        velocity= Vector2(0.7,0)
        particle_amount= 10
        movement_variency= 4
        added_momentum= momentum/ particle_amount*2

        for i in range(0,particle_amount):
            velocity= velocity.rotate(180*i/particle_amount)
            
            
            self.particle_mass= self.radius
            m1= Mover(self.particle_mass,deepcopy(position),velocity* randint(0,movement_variency) + added_momentum/self.particle_mass)
            m2= Mover(self.particle_mass,deepcopy(position), (velocity*-1)* randint(0,movement_variency) +added_momentum/ self.particle_mass )

            self.particles.append(m1)
            self.particles.append(m2)


        self.start()
    
    
class ChainParticles(ParticleSystem):
    def __init__(self, position, height,win_height) -> None:
        super().__init__()
        self.particles= []
        self.duration = 0.5
        self.position= position
        self.threshold= 1
        self.radius= 25

        particle_period= 40
        particle_amount= int(height/particle_period)
        x= position.x
        particle_mass= 10
        for i in range(0,particle_amount):
            particle= Mover(particle_mass,Vector2(x,win_height-height*(i/particle_amount)),Vector2(float(randint(-1,1)/3),0))
            self.particles.append(particle)

        self.start()

class ShooterParticles(ParticleSystem):

    def __init__(self,position, sh_radius) -> None:
        super().__init__()
        self.particles= []
        self.duration = 2
        self.threshold= 1
        self.radius= 25

        particle_amount= 20

        direction= Vector2(1,0)
        for i in range(0,particle_amount):
            direction= direction.rotate(360*(i/particle_amount))
            particle_position1= direction* sh_radius/3
            particle_position2= direction* sh_radius*2/3
            particle_position3= direction*sh_radius

            print(particle_position1,particle_position2,particle_position3)

            self.particles.append(Mover(10,particle_position1+ deepcopy(position)))
            self.particles.append(Mover(10,particle_position2+ deepcopy(position)))
            self.particles.append(Mover(10,particle_position3+ deepcopy(position)))


        self.start()
        


