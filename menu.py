from PPlay.sprite import Sprite
from PPlay.window import Window
from jogo_class import Jogo
import os
import sys

def get_save_path(file_name):
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(application_path, file_name)

class Menu:
    def __init__(self, janela, teclado, mouse):
        self.janela = janela
        self.teclado = teclado
        self.mouse = mouse
        self.background = Sprite(r"assets\background.jpg")
        self.facil = Sprite(r"assets\facil.png")
        self.medio = Sprite(r"assets\medio.png")
        self.dificil = Sprite(r"assets\dificil.png")
        self.medio_locked = Sprite(r"assets\nivel2locked.png")
        self.dificil_locked = Sprite(r"assets\nivel3locked.png")
        
        self.facil.set_position(self.janela.width/2 - self.facil.width/2, self.janela.height - 600 - self.facil.height/2)
        self.medio.set_position(self.janela.width/2 - self.medio.width/2, self.janela.height - 350 - self.medio.height/2)
        self.dificil.set_position(self.janela.width/2 - self.dificil.width/2, self.janela.height - 100 - self.dificil.height/2)
        self.medio_locked.set_position(self.janela.width/2 - self.medio_locked.width/2, self.janela.height - 350 - self.medio_locked.height/2)
        self.dificil_locked.set_position(self.janela.width/2 - self.dificil_locked.width/2, self.janela.height - 100 - self.dificil_locked.height/2)
        
        self.jogo = Jogo(self.janela, self.teclado, self.mouse)

    def dificuldade(self):
        entry_time = self.janela.time_elapsed()
        cooldown_duration = 200
        
        caminho_do_progresso = get_save_path('progresso.txt')
        try:
            with open(caminho_do_progresso, "r") as arquivo:
                estado = arquivo.read().strip()
        except FileNotFoundError:
            with open(caminho_do_progresso, "w") as arquivo:
                arquivo.write("1")
            estado = "1"

        while True:
            self.background.draw()
            self.facil.draw()
            
            if estado == "1":
                self.medio_locked.draw()
                self.dificil_locked.draw()
            elif estado == "2":
                self.medio.draw()
                self.dificil_locked.draw()
            elif estado == "3":
                self.medio.draw()
                self.dificil.draw()

            can_click = self.janela.time_elapsed() > entry_time + cooldown_duration
            if can_click:
                if self.mouse.is_over_object(self.facil) and self.mouse.is_button_pressed(1):
                    while self.mouse.is_button_pressed(1):
                        self.janela.update()
                    self.jogo.jogo1()
                    break

                if self.mouse.is_over_object(self.medio) and self.mouse.is_button_pressed(1) and estado != "1":
                    while self.mouse.is_button_pressed(1):
                        self.janela.update()
                    self.jogo.jogo2()
                    break

                if self.mouse.is_over_object(self.dificil) and self.mouse.is_button_pressed(1) and estado == "3":
                    while self.mouse.is_button_pressed(1):
                        self.janela.update()
                    self.jogo.jogo3()
                    break

            if Window.get_keyboard().key_pressed("ESC"):
                break
            
            self.janela.update()

    def ranking(self):
        while True:
            self.janela.set_background_color([195,195,195])
            if Window.get_keyboard().key_pressed("ESC"):
                break
            self.janela.update()

    def sair(self):
        exit()
