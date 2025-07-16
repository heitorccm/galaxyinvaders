from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.sound import *
from PPlay.window import Window
from nave_class import Nave
from menu import Menu
from jogo_class import Jogo
from PPlay.animation import *
import os, sys
dirpath = os.getcwd()
sys.path.append(dirpath)
if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)
janela = Window(1280, 720)
janela.set_title("Galaxy Invaders")
teclado = Window.get_keyboard()
mouse = Window.get_mouse()
background = Sprite(r"assets\background.jpg")
logo = Sprite(r"assets\logo.png")
logo.set_position(janela.width/2 - logo.width/2, janela.height - 570 - logo.height/2)
jogar = Sprite(r"assets\jogar.png")
sair = Sprite(r"assets\sair.png")
jogar.set_position(janela.width/2 - jogar.width/2, janela.height - 300 - jogar.height/2)
sair.set_position(janela.width/2 - sair.width/2, janela.height - 100 - sair.height/2)
menu = Menu(janela, teclado, mouse)
jogo_class = Jogo(janela, teclado, mouse)
while True:
    background.draw()
    logo.draw()
    jogar.draw()
    sair.draw()
    if mouse.is_over_object(jogar) and mouse.is_button_pressed(1):
      menu.dificuldade()
    if mouse.is_over_object(sair) and mouse.is_button_pressed(1):
      menu.sair()
    janela.update()