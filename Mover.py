from pygame import Vector2

class Mover:
    def __init__ (self,mass,position= Vector2(0,0),velocity= Vector2(0,0), accelaration= Vector2(0,0)) -> None:
        self.mass= mass
        self.position= position
        self.velocity= velocity
        self.accelaration= accelaration
        
    def update(self):
        self.velocity += self.accelaration 
        self.position += self.velocity 

        self.accelaration *= 0

    def applyForce(self, force):
        self.accelaration += force/ self.mass

    def momentum(self):
        return self.velocity * self.mass
    
