import random
import os
import sys
from PPlay.window import *
from PPlay.sprite import *
from PPlay.sound import *
from tiro_class import Tiro, TiroInimigo
from nave_class import Nave
from inimigo_class import Leve, Pesado, MeteoroG, MeteoroP, Boss
from gameover import GameOver

def get_save_path(file_name):
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)
    return os.path.join(application_path, file_name)

class Jogo:
    def __init__(self,janela,teclado,mouse):
        self.janela=janela
        self.teclado=teclado
        self.mouse=mouse
        self.game_over = GameOver(self.janela, self.teclado, self.mouse)

    def jogo1(self):
        musica_fundo = Sound(r"assets\fundo.mp3")
        musica_fundo.set_volume(20)
        musica_fundo.play()
        efeito_tiro = Sound(r"assets\tiro.mp3")
        efeito_tiro.set_volume(30)
        cronometro=0
        cronometro1 = 0
        cronometro2 = 0
        cronometro3 = 0
        self.nave=Nave(0,self.janela.height/2,400)
        tiros=[]
        inimigos=[]
        meteoros=[]
        velocidade_cenario = 200
        pontos = 0
        tirosinimigos = []
        level_2_unlocked_this_session = False
        lista = [
            r"assets\backgrounds\azul\background (1).png",
            r"assets\backgrounds\azul\background (2).png",
            r"assets\backgrounds\azul\background (3).png",
            r"assets\backgrounds\azul\background (5).png",
            r"assets\backgrounds\azul\background (6).png",
        ]
        imagem = random.choice(lista)
        
        caminho_background_txt = get_save_path('background.txt')
        with open(caminho_background_txt, "w") as arquivo:
            arquivo.write(imagem)
            
        self.background = Sprite(imagem)
        self.background1 = Sprite(imagem)
        self.background.set_position(0,0)
        self.background1.set_position(1280,0)
        tempo_inicial = self.janela.time_elapsed()
        
        caminho_do_progresso = get_save_path('progresso.txt')
        print(f"Caminho do arquivo de progresso: {caminho_do_progresso}")

        while True:
            cronometroi = random.randint(3000, 4500)
            delta=self.janela.delta_time()
            fps=int(1/delta) if delta>0 else 0
            tempo_partida_ms = self.janela.time_elapsed() - tempo_inicial
            tempos = float(tempo_partida_ms / 1000)
            self.background.x -= velocidade_cenario * delta
            self.background1.x -= velocidade_cenario * delta
            if self.background.x + self.background.width <= 0:
                self.background.x = self.background1.x + self.background1.width
            if self.background1.x + self.background1.width <= 0:
                self.background1.x = self.background.x + self.background.width
            self.background.draw()
            self.background1.draw()
            self.janela.draw_text(f"FPS: {fps}",1150,10,size=20,color=(255,255,255), font_name=r"assets\fonte.otf")
            if tempos < 60:
                self.janela.draw_text(f"{tempos:.2f}",self.janela.width/2,10,size=20,color=(255,255,255), font_name=r"assets\fonte.otf")
            else:
                minutos = int(tempos // 60)
                segundos = int(tempos % 60)
                self.janela.draw_text(f"{minutos:02d}:{segundos:02d}",self.janela.width/2,10,size=20,color=(255,255,255), font_name=r"assets\fonte.otf")
            if self.teclado.key_pressed("UP"):
                self.nave.move_up(self.janela.delta_time())
            else: 
                chao = 610
                if self.nave.sprite.y < chao:
                    self.nave.move_down(delta)
            self.nave.draw()
            if tempos < 10:
                self.janela.draw_text("FASE DE DESTRUIÇÃO",self.janela.width/2 - 300,40,size=20,color=(255,255,255), font_name=r"assets\fonte.otf")
                self.janela.draw_text("DESTRUA AS NAVES INIMIGAS. VOCÊ PRECISA DE 10 PONTOS PARA PASSAR DE FASE.",self.janela.width/2 - 300,60,size=20,color=(255,255,255), font_name=r"assets\fonte.otf")
                self.janela.draw_text("NAVES PESADAS VALEM 2 PONTOS",self.janela.width/2 - 300,80,size=20,color=(255,255,255), font_name=r"assets\fonte.otf")
            if self.nave.sprite.y >= chao:
                self.nave.lock1()
            if self.nave.sprite.y <= -50:
                self.nave.lock2()
            if self.teclado.key_pressed("SPACE") and cronometro == 0:
                cronometro = self.janela.time_elapsed()
                tiros.append(Tiro(self.nave.sprite.x + 100, self.nave.sprite.y, 200))
                efeito_tiro.play()
            if cronometro + 2000 <= self.janela.time_elapsed():
                cronometro = 0
            for tiro in tiros:
                tiro.move(delta) 
                tiro.draw()
                if tiro.sprite.x > 1280:
                    tiros.remove(tiro)
            if cronometro1 <= 0:
                chance = random.randint(0,100)
                if chance < 70:
                    inimigos.append(Leve(1,350))
                    cronometro1 = self.janela.time_elapsed()
                else:
                    inimigos.append(Pesado(2,100))
                    cronometro1 = self.janela.time_elapsed()
            if cronometro1 + 3000 <= self.janela.time_elapsed():
                cronometro1 = 0
            if cronometro2 <= 0:
                chance = random.randint(0,100)
                if chance < 70:
                    meteoros.append(MeteoroP(500, 1280, random.randint(0, 600)))
                    cronometro2 = self.janela.time_elapsed()
                else:
                    meteoros.append(MeteoroG(300, 1280, random.randint(0, 600)))
                    cronometro2 = self.janela.time_elapsed()
            if cronometro2 + cronometroi <= self.janela.time_elapsed():
                cronometro2 = 0
            if cronometro3 <= 0:
                for inimigo in inimigos[:]:
                    if isinstance(inimigo, Pesado):
                        tirosinimigos.append(TiroInimigo(inimigo.sprite.x - 50, inimigo.sprite.y + 20, 400))
                        cronometro3 = self.janela.time_elapsed()
            if cronometro3 + 4000 <= self.janela.time_elapsed():
                cronometro3 = 0
            for tiro in tirosinimigos:
                tiro.draw()
                tiro.move(delta)
                if tiro.sprite.x < -50:
                    tirosinimigos.remove(tiro)
                if tiro.sprite.collided_perfect(self.nave.sprite):
                    musica_fundo.stop()
                    self.game_over.gameover()
                    return
            for meteoro in meteoros[:]:
                meteoro.move(delta)
                meteoro.draw()
                if meteoro.sprite.x < -150:
                    meteoros.remove(meteoro)
                if meteoro.sprite.collided_perfect(self.nave.sprite):
                    musica_fundo.stop()
                    self.game_over.gameover()
                    return
            for meteoro in meteoros:
                for tiro in tiros:
                    if tiro.sprite.collided_perfect(meteoro.sprite):
                        tiros.remove(tiro)
            for inimigo in inimigos[:]:
                inimigo.move(delta)
                inimigo.draw()
                for tiro in tiros[:]:
                    if tiro.sprite.collided_perfect(inimigo.sprite):
                        inimigo.take_dmg()
                        tiros.remove(tiro)
                if inimigo.vida == 0:
                    inimigos.remove(inimigo)
                    if isinstance(inimigo, Pesado):
                        pontos += 2
                    elif isinstance(inimigo, Leve):
                        pontos += 1
                if inimigo.sprite.x < -150:
                    inimigos.remove(inimigo)
                if inimigo.sprite.collided_perfect(self.nave.sprite):
                    musica_fundo.stop()
                    self.game_over.gameover()
                    return
            
            try:
                with open(caminho_do_progresso, "r") as arquivo:
                    conteudo = arquivo.read().strip()
            except FileNotFoundError:
                with open(caminho_do_progresso, "w") as arquivo:
                    arquivo.write("1")
                conteudo = "1"
            
            if not level_2_unlocked_this_session and conteudo == "1" and pontos >= 10:
                with open(caminho_do_progresso, "w") as arquivo:
                    arquivo.write("2")
                conteudo = "2"
                level_2_unlocked_this_session = True
            
            if level_2_unlocked_this_session:
                self.janela.draw_text("Parabéns! Você desbloqueou o próximo nível!", 300, 30, size=30, color=(0, 255, 0), font_name=r"assets\fonte.otf")

            if Window.get_keyboard().key_pressed("ESC"):
                musica_fundo.stop()
                break
            self.janela.draw_text(f"Pontos: {pontos}", 10, 10, size=20, color=(255, 255, 255), font_name=r"assets\fonte.otf")
            self.janela.update()

    def jogo2(self):
        musica_fundo = Sound(r"assets\fundo.mp3")
        musica_fundo.set_volume(20)
        musica_fundo.play()
        efeito_tiro = Sound(r"assets\tiro.mp3")
        efeito_tiro.set_volume(30)
        cronometro=0
        cronometro1 = 0
        cronometro2 = 0
        cronometro3 = 0
        self.nave=Nave(0,self.janela.height/2,400)
        tiros=[]
        inimigos=[]
        meteoros=[]
        velocidade_cenario = 200
        pontos = 0
        tirosinimigos = []
        level_3_unlocked_this_session = False
        
        caminho_background_txt = get_save_path('background.txt')
        print(f"Caminho do arquivo de progresso: {get_save_path('progresso.txt')}")
        try:
            with open(caminho_background_txt, "r") as arquivo:
                imagem = arquivo.read()
        except FileNotFoundError:
             imagem = r"assets\backgrounds\azul\background (1).png"

        self.background = Sprite(imagem)
        self.background1 = Sprite(imagem)
        self.background.set_position(0,0)
        self.background1.set_position(1280,0)
        tempo_inicial = self.janela.time_elapsed()
        
        while True:
            cronometroi = random.randint(4000, 5000)
            delta=self.janela.delta_time()
            fps=int(1/delta) if delta>0 else 0
            tempo_partida_ms = self.janela.time_elapsed() - tempo_inicial
            tempos = float(tempo_partida_ms / 1000)
            self.background.x -= velocidade_cenario * delta
            self.background1.x -= velocidade_cenario * delta
            if self.background.x + self.background.width <= 0:
                self.background.x = self.background1.x + self.background1.width
            if self.background1.x + self.background1.width <= 0:
                self.background1.x = self.background.x + self.background.width
            self.background.draw()
            self.background1.draw()
            self.janela.draw_text(f"FPS: {fps}",1150,10,size=20,color=(255,255,255), font_name=r"assets\fonte.otf")
            if tempos < 60:
                self.janela.draw_text(f"{tempos:.2f}",self.janela.width/2,10,size=20,color=(255,255,255), font_name=r"assets\fonte.otf")
            else:
                minutos = int(tempos // 60)
                segundos = int(tempos % 60)
                self.janela.draw_text(f"{minutos:02d}:{segundos:02d}",self.janela.width/2,10,size=20,color=(255,255,255), font_name=r"assets\fonte.otf")
            if self.teclado.key_pressed("UP"):
                self.nave.move_up(self.janela.delta_time())
            else: 
                chao = 610
                if self.nave.sprite.y < chao:
                    self.nave.move_down(delta)
            self.nave.draw()
            if tempos < 10:
                self.janela.draw_text("FASE DE FUGA",self.janela.width/2 - 300,40,size=20,color=(255,255,255), font_name=r"assets\fonte.otf")
                self.janela.draw_text("DESVIE DE NAVES INIMIGAS DURANTE 90 SEGUNDOS E PASSE DE FASE",self.janela.width/2 - 300,60,size=20,color=(255,255,255), font_name=r"assets\fonte.otf")
            if self.nave.sprite.y >= chao:
                self.nave.lock1()
            if self.nave.sprite.y <= -50:
                self.nave.lock2()
            if self.teclado.key_pressed("SPACE") and cronometro == 0:
                cronometro = self.janela.time_elapsed()
                tiros.append(Tiro(self.nave.sprite.x + 100, self.nave.sprite.y, 200))
                efeito_tiro.play()
            if cronometro + 3000 <= self.janela.time_elapsed():
                cronometro = 0
            for tiro in tiros:
                tiro.move(delta) 
                tiro.draw()
                if tiro.sprite.x > 1280:
                    tiros.remove(tiro)
            if cronometro1 <= 0:
                chance = random.randint(0,100)
                if chance < 70:
                    inimigos.append(Leve(2,350))
                    cronometro1 = self.janela.time_elapsed()
                else:
                    inimigos.append(Pesado(2,50))
                    cronometro1 = self.janela.time_elapsed()
            if cronometro1 + 5500 <= self.janela.time_elapsed():
                cronometro1 = 0
            if cronometro2 <= 0:
                chance = random.randint(0,100)
                if chance < 70:
                    meteoros.append(MeteoroP(500, 1280, random.randint(0, 600)))
                    cronometro2 = self.janela.time_elapsed()
                else:
                    meteoros.append(MeteoroG(300, 1280, random.randint(0, 600)))
                    cronometro2 = self.janela.time_elapsed()
            if cronometro2 + cronometroi <= self.janela.time_elapsed():
                cronometro2 = 0
            if cronometro3 <= 0:
                for inimigo in inimigos[:]:
                    if isinstance(inimigo, Pesado):
                        tirosinimigos.append(TiroInimigo(inimigo.sprite.x - 50, inimigo.sprite.y + 20, 400))
                        cronometro3 = self.janela.time_elapsed()
            if cronometro3 + 2500 <= self.janela.time_elapsed():
                cronometro3 = 0
            for tiro in tirosinimigos:
                tiro.draw()
                tiro.move(delta)
                if tiro.sprite.x < -50:
                    tirosinimigos.remove(tiro)
                if tiro.sprite.collided_perfect(self.nave.sprite):
                    musica_fundo.stop() 
                    self.game_over.gameover()
                    return
            for meteoro in meteoros[:]:
                meteoro.move(delta)
                meteoro.draw()
                if meteoro.sprite.x < -150:
                    meteoros.remove(meteoro)
                if meteoro.sprite.collided_perfect(self.nave.sprite):
                    musica_fundo.stop()
                    self.game_over.gameover()
                    return
            for meteoro in meteoros:
                for tiro in tiros:
                    if tiro.sprite.collided_perfect(meteoro.sprite):
                        tiros.remove(tiro)
            for inimigo in inimigos[:]:
                inimigo.move(delta)
                inimigo.draw()
                for tiro in tiros[:]:
                    if tiro.sprite.collided_perfect(inimigo.sprite):
                        inimigo.take_dmg()
                        tiros.remove(tiro)
                if inimigo.vida == 0:
                    inimigos.remove(inimigo)
                    pontos += 1
                if inimigo.sprite.x < -150:
                    inimigos.remove(inimigo)
                if inimigo.sprite.collided_perfect(self.nave.sprite):
                    musica_fundo.stop()
                    self.game_over.gameover()
                    return
            
            caminho_do_progresso = get_save_path('progresso.txt')
            try:
                with open(caminho_do_progresso, "r") as arquivo:
                    conteudo = arquivo.read().strip()
            except FileNotFoundError:
                with open(caminho_do_progresso, "w") as arquivo:
                    arquivo.write("1")
                conteudo = "1"
            
            if not level_3_unlocked_this_session and conteudo == "2" and tempos > 90:
                with open(caminho_do_progresso, "w") as arquivo:
                    arquivo.write("3")
                conteudo = "3"
                level_3_unlocked_this_session = True

            if level_3_unlocked_this_session:
                self.janela.draw_text("Parabéns! Você desbloqueou o nível final!", 300, 30, size=30, color=(0, 255, 0), font_name=r"assets\fonte.otf")

            if Window.get_keyboard().key_pressed("ESC"):
                musica_fundo.stop()
                break
            self.janela.draw_text(f"Pontos: {pontos}", 10, 10, size=20, color=(255, 255, 255), font_name=r"assets\fonte.otf")
            self.janela.update()

    def jogo3(self):
        musica_fundo = Sound(r"assets\fundo.mp3")
        musica_fundo.set_volume(20)
        musica_fundo.play()
        efeito_tiro = Sound(r"assets\tiro.mp3")
        efeito_tiro.set_volume(30)
        cronometro=0
        cronometro1 = 0
        cronometro2 = 0
        cronometro3 = 0
        z = 0
        self.nave=Nave(0,self.janela.height/2,400)
        tiros=[]
        inimigos=[]
        meteoros=[]
        velocidade_cenario = 200
        pontos = 10
        tirosinimigos = []

        caminho_background_txt = get_save_path('background.txt')
        print(f"Caminho do arquivo de progresso: {get_save_path('progresso.txt')}")
        try:
            with open(caminho_background_txt, "r") as arquivo:
                imagem = arquivo.read()
        except FileNotFoundError:
             imagem = r"assets\backgrounds\azul\background (1).png"

        self.background = Sprite(imagem)
        self.background1 = Sprite(imagem)
        self.background.set_position(0,0)
        self.background1.set_position(1280,0)
        tempo_inicial = self.janela.time_elapsed()
        
        while True:
            sorteador = random.randint(0,1)
            if sorteador == 0:
                sorteador1 = random.randint(0,200)
            elif sorteador == 1:
                sorteador1 = random.randint(500, 650)
            cronometroi = random.randint(2000, 3500)
            delta=self.janela.delta_time()
            fps=int(1/delta) if delta>0 else 0
            tempo_partida_ms = self.janela.time_elapsed() - tempo_inicial
            tempos = float(tempo_partida_ms / 1000)
            self.background.x -= velocidade_cenario * delta
            self.background1.x -= velocidade_cenario * delta
            if self.background.x + self.background.width <= 0:
                self.background.x = self.background1.x + self.background1.width
            if self.background1.x + self.background1.width <= 0:
                self.background1.x = self.background.x + self.background.width
            self.background.draw()
            self.background1.draw()
            self.janela.draw_text(f"FPS: {fps}",1150,10,size=20,color=(255,255,255), font_name=r"assets\fonte.otf")
            if tempos < 60:
                self.janela.draw_text(f"{tempos:.2f}",self.janela.width/2,10,size=20,color=(255,255,255), font_name=r"assets\fonte.otf")
            else:
                minutos = int(tempos // 60)
                segundos = int(tempos % 60)
                self.janela.draw_text(f"{minutos:02d}:{segundos:02d}",self.janela.width/2,10,size=20,color=(255,255,255), font_name=r"assets\fonte.otf")
            if self.teclado.key_pressed("UP"):
                self.nave.move_up(self.janela.delta_time())
            else: 
                chao = 610
                if self.nave.sprite.y < chao:
                    self.nave.move_down(delta)
            self.nave.draw()
            if self.nave.sprite.y >= chao:
                self.nave.lock1()
            if self.nave.sprite.y <= -50:
                self.nave.lock2()
            if self.teclado.key_pressed("SPACE") and cronometro == 0:
                cronometro = self.janela.time_elapsed()
                tiros.append(Tiro(self.nave.sprite.x + 100, self.nave.sprite.y, 200))
                efeito_tiro.play()
            if cronometro + 2000 <= self.janela.time_elapsed():
                cronometro = 0
            for tiro in tiros:
                tiro.move(delta) 
                tiro.draw()
                if tiro.sprite.x > 1280:
                    tiros.remove(tiro)
            if z == 0:
                inimigos.append(Boss())
                z += 1
            if cronometro2 <= 0:
                chance = random.randint(0,100)
                if chance < 70:
                    meteoros.append(MeteoroP(500, 1280, sorteador1))
                    cronometro2 = self.janela.time_elapsed()
                else:
                    meteoros.append(MeteoroG(300, 1280, sorteador1))
                    cronometro2 = self.janela.time_elapsed()
            if cronometro2 + cronometroi <= self.janela.time_elapsed():
                cronometro2 = 0
            if cronometro3 <= 0:
                for inimigo in inimigos[:]:
                    if isinstance(inimigo, Boss):
                        tiro_range1 = random.choice([inimigo.sprite.y + 200,inimigo.sprite.y + 250])
                        tiro_range2 = random.choice([inimigo.sprite.y + 300,inimigo.sprite.y + 350])
                        tiro_range3 = random.choice([inimigo.sprite.y + 400,inimigo.sprite.y + 450])
                        tirosinimigos.append(TiroInimigo(inimigo.sprite.x - 50, tiro_range1, 400))
                        tirosinimigos.append(TiroInimigo(inimigo.sprite.x - 50, tiro_range2, 400))
                        tirosinimigos.append(TiroInimigo(inimigo.sprite.x - 50, tiro_range3, 400))
                        cronometro3 = self.janela.time_elapsed()
            if cronometro3 + 3000 <= self.janela.time_elapsed():
                cronometro3 = 0
            for tiro in tirosinimigos:
                tiro.draw()
                tiro.move(delta)
                if tiro.sprite.x < -50:
                    tirosinimigos.remove(tiro)
                if tiro.sprite.collided_perfect(self.nave.sprite):
                    musica_fundo.stop() 
                    self.game_over.gameover()
                    return
            for meteoro in meteoros[:]:
                meteoro.move(delta)
                meteoro.draw()
                if meteoro.sprite.x < -150:
                    meteoros.remove(meteoro)
                if meteoro.sprite.collided_perfect(self.nave.sprite):
                    musica_fundo.stop()
                    self.game_over.gameover()
                    return
            for meteoro in meteoros:
                for tiro in tiros:
                    if tiro.sprite.collided_perfect(meteoro.sprite):
                        tiros.remove(tiro)
            for inimigo in inimigos[:]:
                inimigo.draw()
                for tiro in tiros[:]:
                    if tiro.sprite.collided_perfect(inimigo.sprite):
                        inimigo.take_dmg()
                        tiros.remove(tiro)
                if inimigo.vida == 0:
                    inimigos.remove(inimigo)
                    self.game_over.vitoria()
                if inimigo.sprite.x < -150:
                    inimigos.remove(inimigo)
                if inimigo.sprite.collided_perfect(self.nave.sprite):
                    musica_fundo.stop()
                    self.game_over.gameover()
                    return
            if Window.get_keyboard().key_pressed("ESC"):
                musica_fundo.stop()
                break
            for inimigo in inimigos:
                self.janela.draw_text(f"VIDAS: {inimigo.vida}", 10, 10, size=20, color=(255, 255, 255), font_name=r"assets\fonte.otf")
            self.janela.update()
