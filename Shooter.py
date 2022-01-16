from pygame import Vector2
from Mover import Mover

class Shooter(Mover):

    def __init__(self, position, radius,speed) -> None:
        super().__init__(1, position)
        self.radius= radius
        self.speed= speed

    def move_right(self,dt):
        self.position.x += self.speed*dt
        

    def move_left(self,dt):
        self.position.x -= self.speed*dt

    