from PPlay.sprite import Sprite
class Tiro:
    def __init__(self, x1, y1, speed):
        self.sprite = Sprite(r"assets\tiro.png")
        self.sprite.set_position(x1,y1)
        self.speed = speed
    def move(self, delta_time):
        self.sprite.x += self.speed * delta_time
    def draw(self):
        self.sprite.draw()
class TiroInimigo:
    def __init__(self, x1, y1, speed):
        self.sprite = Sprite(r"assets\tiroi.png")
        self.sprite.set_position(x1,y1)
        self.speed = speed
    def move(self, delta_time):
        self.sprite.x -= self.speed * delta_time
    def draw(self):
        self.sprite.draw()
