from pygame import Vector2
import time
from Mover import Mover
from random import randint
from copy import deepcopy


class ParticleManager:

    def __init__(self) ->None:
        self.particle_systems= []

    def add_particles(self,particles):
        self.particle_systems.append(particles)

class Particles:
    def __init__(self, duration, position, momentum) -> None:
        self.particles= []
        self.duration= duration
        self.threshold= 0.4

        velocity= Vector2(0.8,0)
        particle_amount= 10
        added_momentum= momentum/ particle_amount*2

        for i in range(0,particle_amount):
            velocity= velocity.rotate(180*i/particle_amount)
            
            
            particle_mass= 10
            m1= Mover(particle_mass,deepcopy(position),velocity* randint(1,4) + added_momentum/particle_mass)
            m2= Mover(particle_mass,deepcopy(position), (velocity*-1)* randint(1,4) +added_momentum/ particle_mass )

            self.particles.append(m1)
            self.particles.append(m2)

        for particle in self.particles:
            print(particle.position, particle.velocity)

        self.start()
            
    def start(self):
        self.init_time= time.time()
    
        
    def elapsed_ratio(self):
        return (time.time()- self.init_time) / self.duration 

    def disappeared(self):
        return self.elapsed_ratio() > self.threshold
    
