from PPlay.sprite import *
from PPlay.window import *
import random
class Inimigo:
    def __init__(self):
            self.y = random.randint(0,600)
            self.x = 1200
            self.speed = 100
            self.vida = 1
            self.sprite = None 
            self.spritetiro = Sprite(r"assets\tiroi.png")
    def draw(self):
        self.sprite.draw()
    def take_dmg(self):
        self.vida -= 1
    def move(self, delta):
        self.sprite.x -= self.speed * delta
    def shoot(self,delta):
        self.spritetiro.set_position(self.sprite.x - 50, self.sprite.y + 20)
        self.spritetiro.draw()
        self.spritetiro.x += 500 * delta
class Leve(Inimigo):
     def __init__(self, vida, speed):
          super().__init__()
          self.sprite = Sprite(r"assets\inimigo_l.png")
          self.sprite.set_position(self.x, self.y)
          self.vida = vida
          self.speed = speed
class Pesado(Inimigo):
     def __init__(self, vida, speed):
          super().__init__() 
          self.sprite = Sprite(r"assets\inimigo_p.png")
          self.sprite.set_position(self.x, self.y)
          self.vida = vida
          self.speed = speed
class MeteoroG(Inimigo):
     def __init__(self,speed, x, y):
          super().__init__()
          self.sprite = Sprite(r"assets\meteoroG.png")
          self.sprite.set_position(x, y)
          self.speed = speed
class MeteoroP(Inimigo):
     def __init__(self,speed, x, y):
          super().__init__()
          self.sprite = Sprite(r"assets\meteorop.png")
          self.sprite.set_position(x, y)
          self.speed = speed
class Boss(Inimigo):
    def __init__(self):
        super().__init__()
        self.sprite = Sprite(r"assets\naveboss.png")
        self.sprite.set_position(600, 0)
        self.vida = 50
