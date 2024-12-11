from random import randint
import pygame


class Jugador:
    def __init__(self,nombre,peon) -> None:
        self.nombre=nombre
        self.peon=peon
        self.dinero=35000
        self.propiedades=[]
        self.tarjetas=[]
        self.ubicacion=0
        self.ubicacionStr=str(self.ubicacion)
        self.dados=self.tirarDados()[2]
        self.orden=-1
        self.enTurno=False
        self.preso=False
        self.chacras=0
        self.hipotecadas=0
        self.descansos=0
        self.intentos_salir=0
        print(self.dados)

    def __str__(self) -> str:
        return 'El jugador '+self.nombre+' tiene asignado el peon '+self.peon+' cuenta con $'+str(self.dinero)+' y se encuentra en la posicion '+ str(self.ubicacion)+' su orden es: '+ str(self.orden)

    def tirarDados(self,pantalla=None,x=None,y=None):
        dadoUno=randint(1,6)
        dadoDos=randint(1,6)
        total=dadoUno+dadoDos
        doble=dadoUno==dadoDos
        img_dado1 = pygame.image.load('img/dados/dado_1.jpg').convert()
        pack_dado1 = [1,img_dado1, img_dado1.get_rect()]
        img_dado2 = pygame.image.load('img/dados/dado_2.jpg').convert()
        pack_dado2 = [2,img_dado2, img_dado2.get_rect()]
        img_dado3 = pygame.image.load('img/dados/dado_3.jpg').convert()
        pack_dado3 = [3,img_dado3, img_dado3.get_rect()]
        img_dado4 = pygame.image.load('img/dados/dado_4.jpg').convert()
        pack_dado4 = [4,img_dado4, img_dado4.get_rect()]
        img_dado5 = pygame.image.load('img/dados/dado_5.jpg').convert()
        pack_dado5 = [5,img_dado5, img_dado5.get_rect()]
        img_dado6 = pygame.image.load('img/dados/dado_6.jpg').convert()
        pack_dado6 = [6,img_dado6, img_dado6.get_rect()]
        pack_dados = (pack_dado1, pack_dado2, pack_dado3, pack_dado4, pack_dado5, pack_dado6)
        if pantalla:
            pygame.draw.rect(pantalla,(0,0,0),(x/2-200,y/2-150,400,300),border_radius=25)
            rect_dadoUno = (x/2-150,y/2-100)
            rect_dadoDos = (x/2+50,y/2-100)
            for dado in pack_dados:
                if dado[0] == dadoUno:
                    dado[1] = pygame.transform.scale(dado[1], (100,130))
                    dado[1].set_colorkey((255,255,255))
                    dado[2].center = rect_dadoUno
                    pantalla.blit(dado[1],rect_dadoUno)
                if dado[0] == dadoDos:
                    dado[1] = pygame.transform.scale(dado[1], (100,130))
                    dado[1].set_colorkey((255,255,255))
                    dado[2].center = rect_dadoDos
                    pantalla.blit(dado[1],rect_dadoDos)
            pygame.display.update()
            ver_dados = 0
            while ver_dados<5000:
                ver_dados += 1
                print(ver_dados)
        return dadoUno,dadoDos,total,doble

    def marchePreso(self):
        self.ubicacion=14
        self.preso=True
        self.intentos_salir=3