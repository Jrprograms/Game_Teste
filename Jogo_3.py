import pygame as pg
from pygame.locals import *
import random

pg.init()

#cordenadas
largura = 700
altura = 320
x = 20
y = 281

#leis do jogo
vel_x = 8
vel_y = 10
jump = False
colide = False
jumping = False
ground_collide = True

G = 9

#lvl e key
lvl = 0
key = False

#variaveis extras
    #animacao da fase[2]
animacao1 = True

#defs de desenho

def draw_key(fundo,posicao):
    cor = (255,255,0)
    return pg.draw.rect(fundo,cor,posicao)

def draw_obs(fundo,cor,posicao):
    return pg.draw.rect(fundo,cor,posicao)

def draw_portal(fundo,cor,posicao):
    return pg.draw.rect(fundo,cor,posicao)

def player(fundo,cor,posicao):
    return pg.draw.rect(fundo,cor,posicao)


#player sprite

def fase(lvl):

    if lvl == 0:
        cenario = [draw_obs(tela, (0,255,0), (400,270,20,40)), 
                    draw_obs(tela, (0,255,0), (200,270,20,40))
             ]
        if key is False:
            return [cenario[0],cenario[1], draw_key(tela,(600,270,20,20))]
        elif key is True:
            return [cenario[0],cenario[1], draw_portal(tela, (0,0,255), (0,270,40,30))] 
    
    if lvl == 1:
        cenario = [draw_obs(tela, (0,255,0), (100,260,20,40)),
                   draw_obs(tela, (0,0,0), (180,299,50,21)),
                   draw_obs(tela,(100,70,0), (650,270,30,30)),
                   draw_obs(tela, (100,70,0), (580,240,30,30))]
        if key is False:
            return [cenario[0],cenario[1] , cenario[2],cenario[3],draw_key(tela,(650,160,20,20))]
        
        elif key is True:
           return [cenario[0],cenario[1] , cenario[2],cenario[3],draw_portal(tela, (0,0,255), (0,270,40,30))]
    
    if lvl == 2:
        if animacao1 is True:
            
            pg.font.init()
            fonte = pg.font.get_default_font()
            fontesys = pg.font.SysFont(fonte,30,True,True)
            txttela = fontesys.render(("Loading" + "."*random.randint(1,3)),True,(0,0,0))

            return [
                pg.draw.circle(tela,(0,0,0),(350,280),(random.randint(30,75))),
                tela.blit(txttela,(0,0))
            ]
        elif key is False:
            #desenhando novo fundo
            fundo = pg.image.load("./src/fundo.jpg")
            fundo = pg.transform.scale(fundo,(largura,altura))
            fundo_player = fundo
            return[
                tela.blit(fundo,(0,0))
            ]



tela = pg.display.set_mode((largura, altura))
fundo_player = tela
pg.display.set_caption('Game')
relogio = pg.time.Clock()

while True:
    tela.fill((0,0,200))
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            exit()
        if event.type == KEYDOWN:
            #pulo
            if event.key == K_w and jump == 0:
                jump = True

    if pg.key.get_pressed()[K_a] and x > 0:
       x -= vel_x
    if pg.key.get_pressed()[K_d] and x < 680:
        x += vel_x
    
    #pulo
    if jump is True:
        y -= vel_y
        vel_y -= 1
        jumping = True
        if vel_y < - 10:
            jump = False
            vel_y = 10
            jumping = False 
    
    #player
    player = pg.draw.rect(fundo_player, (255,0,0), (x,y,20,20))

    #chão
    ground = pg.draw.rect(tela, (170,170,170), (0,300,largura,20))


    #colisões e obstáculos(por fase):
    if lvl == 0:
        obstáculos = fase(lvl)
        if key is True:
            if player.colliderect(obstáculos[2]):
                lvl = 1
        if key is False and player.colliderect(obstáculos[2]):
            key = True          
        if player.colliderect(obstáculos[0]) or player.colliderect(obstáculos[1]):
                print('Game Over')
                key = False
                x = 20
        if lvl == 1:
            key = False
            x = 20
        

    if lvl == 1:
        obstáculos = fase(lvl)
        if player.colliderect(ground):
            ground_collide = True
        #obstaculos
        if player.colliderect(obstáculos[0]) or player.colliderect(obstáculos[1]):
            x = 20
            print('Game Over')
            key = False
        #caixa
        if player.colliderect(obstáculos[2]):
            y = 251
            colide = True
            ground_collide = False
        elif player.colliderect(obstáculos[3]) and ground_collide is False:
            y = 221
            colide = True
        else:
            colide = False

        
        if colide is False and jumping == False:
            y = 281
        
        #chegou no portal
        if key is True:
            if player.colliderect(obstáculos[4]):
                print("chgou aki")
                lvl = 2
                x = 20
                y = 280
                key = False
                print('next lvl')

        #chave
        if player.colliderect(obstáculos[4]):
            key = True


    if lvl == 2:
        obstáculos = fase(lvl)
        if colide is False and jumping == False:
            y = 281

        #incio na animação
        if animacao1 is True:
            x += 5
            if player.colliderect(obstáculos[0]):
                x = 20
                animacao1 = False
        if animacao1 is False and key is False:
            print(fundo_player)
            
    pg.time.delay(30)
    pg.display.update()
