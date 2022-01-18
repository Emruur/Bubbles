
import time
from Mover import Mover
from pygame import Vector2

class Level:

    def __init__(self, level=0, duration= 10) -> None:
        self.level= level
        self.duration= duration
        self.movers= []
        self.shooter_location= None
        self.start_time= time.time()

        

    def start(self):
        self.start_time= time.time()

    #returns a ratio showing how much of the level is completed
    def elapsed(self):
        return (time.time()- self.start_time)/ self.duration

    def lost(self):
        return self.elapsed()>1

    

class LevelManager:
     
    def __init__(self, width,height,shooter_radius) -> None:
        self.levels= []
        self.total_levels= 0
        self.current_level= 5

        l1= Level(1,20)
        l1.movers.append(Mover(80,Vector2(width/2, 300)))
        l1.shooter_location= Vector2(width/2, height-shooter_radius)
        self.levels.append(l1)
        self.total_levels += 1

        l2= Level(2,20)
        l2.movers.append(Mover(40, Vector2(width/4,height/2)))
        l2.movers.append(Mover(40, Vector2(width/2, height/2)))
        l2.movers.append(Mover(40, Vector2(width*3/4, height/2)))
        l2.shooter_location= Vector2(width/2, height-shooter_radius)
        self.levels.append(l2)
        self.total_levels += 1

        l3 = Level(3,20)
        l3.movers.append(Mover(80, Vector2(width/3, 300)))
        l3.movers.append(Mover(80, Vector2(width*2/3, 300)))
        l3.shooter_location= Vector2(width/2, height-shooter_radius)
        self.levels.append(l3)
        self.total_levels += 1

        l4= Level(4,20)
        l4.movers.append(Mover(160,Vector2(width/2,height/2)))
        l4.shooter_location= Vector2(width/2, height-shooter_radius)
        self.levels.append(l4)
        self.total_levels += 1

        l5= Level(5,20)
        l5.movers.append(Mover(80, Vector2(width/4, 200)))
        l5.movers.append(Mover(80, Vector2(width*2/4, 200)))
        l5.movers.append(Mover(80, Vector2(width*3/4, 200)))
        l5.shooter_location= Vector2(width/2, height-shooter_radius)
        self.levels.append(l5)
        self.total_levels += 1

        l6= Level(6,10)
        l6.movers.append(Mover(40, Vector2(width/5, 120)))
        l6.movers.append(Mover(40, Vector2(width*2/5, 120)))
        l6.movers.append(Mover(40, Vector2(width*3/5, 120)))
        l6.movers.append(Mover(40, Vector2(width*4/5, 120)))
        l6.shooter_location= Vector2(width/5, height-shooter_radius)
        self.levels.append(l6)
        self.total_levels += 1

        l7= Level(7,15)
        l7.movers.append(Mover(40, Vector2(width/3,300),Vector2(20,0)))
        l7.movers.append(Mover(40, Vector2(width*2/3,350),Vector2(-20,0)))
        l7.shooter_location= Vector2(width/5, height-shooter_radius)
        self.levels.append(l7)
        self.total_levels += 1


    def load_level(self):   
        if len(self.levels) <= self.current_level:
            return None
        else:
            level= self.levels[self.current_level]
            self.current_level += 1
            return level

    def reset(self):
        self.current_level= 0



