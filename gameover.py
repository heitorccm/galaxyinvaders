from PPlay.window import Window
from PPlay.sprite import Sprite

class GameOver:
    def __init__(self, janela, teclado, mouse):
        self.janela = janela
        self.teclado = teclado
        self.mouse = mouse
    def gameover(self):
        while True:
            background = Sprite(r"assets\gameover.png")
            background.set_position(0, 0)
            background.draw()
            if Window.get_keyboard().key_pressed("ESC"):
                self.var = 1
                break
            self.janela.update()
    def vitoria(self):
        while True:
            background = Sprite(r"assets\vitória.png")
            background.set_position(0, 0)
            background.draw()
            if Window.get_keyboard().key_pressed("ESC"):
                self.var = 1
                break
            self.janela.update()
    def salvar_pontos(self, pontos):
        with open(r"assets\ranking.txt", "a") as arquivo:
            arquivo.write(f"{pontos}\n")