from pygame import Vector2
import copy

class ChainBullet:

    def __init__(self, bottom_position,mass= 20, top_velocity= Vector2(0,-13)) -> None:
        self.bottom_position = bottom_position
        self.top_velocity= top_velocity
        self.top_position= copy.deepcopy(bottom_position)
        self.anchored= False
        self.anchored_in= None
        self.anchor_duration= 0.5
        self.mass= mass
        self.width= 10
    
    def update(self):
        if not self.anchored:
            self.top_position += self.top_velocity

    def anchor(self, time):
        self.anchored= True
        self.anchored_in= time

    def momentum(self):
        return self.top_velocity*self.mass