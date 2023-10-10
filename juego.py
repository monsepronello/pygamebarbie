import random
import pygame
from pygame.locals import QUIT, KEYDOWN, K_SPACE


horizontal = 800  
vertical = 600  
FPS = 60 
LILA = (182, 149, 192)  
FUCSIA = (255, 0, 255)  



class Pelota:
    def __init__(self, fichero_imagen):
        self.imagen = pygame.image.load(fichero_imagen).convert_alpha()        
        self.ancho, self.alto = self.imagen.get_size() 
        self.x = horizontal / 2 - self.ancho / 2
        self.y = vertical / 2 - self.alto / 2
        self.dir_x = random.choice([-5, 5])
        self.dir_y = random.choice([-5, 5])
        self.puntuacion = 0
        self.puntuacion_ia = 0

    def mover(self):
        self.x += self.dir_x
        self.y += self.dir_y

    def rebotar(self):
        if self.x <= -self.ancho:
            self.reiniciar()
            self.puntuacion_ia += 1
        if self.x >= horizontal:
            self.reiniciar()
            self.puntuacion += 1
        if self.y <= 0:
            self.dir_y = -self.dir_y
        if self.y + self.alto >= vertical:
            self.dir_y = -self.dir_y

    def reiniciar(self):
        self.x = horizontal / 2 - self.ancho / 2
        self.y = vertical/ 2 - self.alto / 2
        self.dir_x = -self.dir_x
        self.dir_y = random.choice([-5, 5])


class Raqueta:
    def __init__(self):
        self.imagen = pygame.image.load("raqueta.png").convert_alpha()
        self.ancho, self.alto = self.imagen.get_size()
        self.x = 0
        self.y = vertical / 2 - self.alto / 2
        self.dir_y = 0

    def mover(self):
        self.y += self.dir_y
        if self.y <= 0:
            self.y = 0
        if self.y + self.alto >= vertical:
            self.y = vertical - self.alto

    def mover_ia(self, pelota):
        if self.y > pelota.y:
            self.dir_y = -3
        elif self.y < pelota.y:
            self.dir_y = 3
        else:
            self.dir_y = 0

        self.y += self.dir_y

    def golpear(self, pelota):
        if (
            pelota.x < self.x + self.ancho
            and pelota.x > self.x
            and pelota.y + pelota.alto > self.y
            and pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -pelota.dir_x
            pelota.x = self.x + self.ancho

    def golpear_ia(self, pelota):
        if (
            pelota.x + pelota.ancho > self.x
            and pelota.x < self.x + self.ancho
            and pelota.y + pelota.alto > self.y
            and pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -pelota.dir_x
            pelota.x = self.x - pelota.ancho



def mostrar_menu(ventana, fuente):
    ventana.fill(LILA)
    titulo = fuente.render("Ping Pong Barbie", True, FUCSIA)
    texto_iniciar = fuente.render("Presiona ESPACIO para iniciar", True, FUCSIA)
    texto_salir = fuente.render("Presiona Q para salir", True, FUCSIA)

    ventana.blit(titulo, (horizontal / 2 - titulo.get_width() / 2, 200))
    ventana.blit(texto_iniciar, (horizontal / 2 - texto_iniciar.get_width() / 2, 300))
    ventana.blit(texto_salir, (horizontal / 2 - texto_salir.get_width() / 2, 350))

    pygame.display.flip()

def main():
    pygame.init()
    ventana = pygame.display.set_mode((horizontal, vertical))
    pygame.display.set_caption("Ping Pong Barbie")
    fuente = pygame.font.Font(None, 60)
    pelota = None
    raqueta_1 = None
    raqueta_2 = None
    jugando = False
    en_menu = True

    
    mostrar_menu(ventana, fuente)

    while en_menu:
        for event in pygame.event.get():
            if event.type == QUIT:
                en_menu = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pelota = Pelota("bola.png")
                    raqueta_1 = Raqueta()
                    raqueta_1.x = 60
                    raqueta_2 = Raqueta()
                    raqueta_2.x = horizontal - 60 - raqueta_2.ancho
                    jugando = True
                    en_menu = False
                elif event.key == pygame.K_q:
                    en_menu = False

    


    while jugando:
        pelota.mover()
        pelota.rebotar()
        raqueta_1.mover()
        raqueta_2.mover_ia(pelota)
        raqueta_1.golpear(pelota)
        raqueta_2.golpear_ia(pelota)
        ventana.fill(LILA)
        ventana.blit(pelota.imagen, (pelota.x, pelota.y))
        ventana.blit(raqueta_1.imagen, (raqueta_1.x, raqueta_1.y))
        ventana.blit(raqueta_2.imagen, (raqueta_2.x, raqueta_2.y))
        texto = f"{pelota.puntuacion} : {pelota.puntuacion_ia}"
        letrero = fuente.render(texto, False, FUCSIA)
        ventana.blit(letrero, (horizontal / 2 - fuente.size(texto)[0] / 2, 50))

        if pelota.puntuacion >= 10 or pelota.puntuacion_ia >= 10:
            jugando = False

        for event in pygame.event.get():
            if event.type == QUIT:
                jugando = False

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    raqueta_1.dir_y = -5
                if event.key == pygame.K_s:
                    raqueta_1.dir_y = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    raqueta_1.dir_y = 0
                if event.key == pygame.K_s:
                    raqueta_1.dir_y = 0


        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
