import pygame
import os
import random
import sys

pygame.init()
pygame.mixer.init()


# Configurações da tela
tela_largura = 500
tela_altura = 800

# Carregar imagens
imagem_cano = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
imagem_chao = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
imagem_background = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

imagens_passaro = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]

# Sons
som_ponto = pygame.mixer.Sound(os.path.join('sounds', 'point.wav'))
som_colisao = pygame.mixer.Sound(os.path.join('sounds', 'hit.wav'))
som_pulo = pygame.mixer.Sound(os.path.join('sounds', 'jump.wav'))

# Fonte
pygame.font.init()
fonte_pontuacao = pygame.font.SysFont("arial", 50)
fonte_menu = pygame.font.SysFont("arial", 40)

# Classe do pássaro
class Passaro:
    imgs = imagens_passaro
    rotacao_maxima = 25
    velocidade_rotacao = 20
    tempo_animacao = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.altura = self.y
        self.angulo = 0
        self.velocidade = 0
        self.tempo = 0
        self.imagem = self.imgs[0]
        self.contador_imagem = 0

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y
        som_pulo.play()

    def mover(self):
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        if deslocamento >= 16:
            deslocamento = 16
        if deslocamento < 0:
            deslocamento -= 2
        self.y += deslocamento

        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.rotacao_maxima:
                self.angulo = self.rotacao_maxima
        else:
            if self.angulo > -90:
                self.angulo -= self.velocidade_rotacao

    def desenhar(self, tela):
        self.contador_imagem += 1

        if self.contador_imagem < self.tempo_animacao:
            self.imagem = self.imgs[0]
        elif self.contador_imagem < self.tempo_animacao * 2:
            self.imagem = self.imgs[1]
        elif self.contador_imagem < self.tempo_animacao * 3:
            self.imagem = self.imgs[2]
        elif self.contador_imagem < self.tempo_animacao * 4:
            self.imagem = self.imgs[1]
        else:
            self.imagem = self.imgs[0]
            self.contador_imagem = 0

        if self.angulo <= -80:
            self.imagem = self.imgs[1]
            self.contador_imagem = self.tempo_animacao * 2

        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

# Classe dos canos
class Cano:
    distancia = 200
    velocidade = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.cano_topo = pygame.transform.flip(imagem_cano, False, True)
        self.cano_base = imagem_cano
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.cano_topo.get_height()
        self.pos_base = self.altura + self.distancia

    def mover(self):
        self.x -= self.velocidade

    def desenhar(self, tela):
        tela.blit(self.cano_topo, (self.x, self.pos_topo))
        tela.blit(self.cano_base, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.cano_topo)
        base_mask = pygame.mask.from_surface(self.cano_base)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if topo_ponto or base_ponto:
            return True
        return False

# Classe do chão
class Chao:
    velocidade = 5
    largura = imagem_chao.get_width()
    imagem = imagem_chao

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.largura

    def mover(self):
        self.x1 -= self.velocidade
        self.x2 -= self.velocidade

        if self.x1 + self.largura < 0:
            self.x1 = self.x2 + self.largura
        if self.x2 + self.largura < 0:
            self.x2 = self.x1 + self.largura

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.imagem, (self.x2, self.y))

# Função desenhar a tela
def desenhar_tela(tela, passaros, canos, chao, pontos, recorde):
    tela.blit(imagem_background, (0, 0))
    for cano in canos:
        cano.desenhar(tela)

    chao.desenhar(tela)

    for passaro in passaros:
        passaro.desenhar(tela)

    texto = fonte_pontuacao.render(f"Pontos: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (tela_largura - 10 - texto.get_width(), 10))

    texto_recorde = fonte_pontuacao.render(f"Recorde: {recorde}", 1, (255, 255, 255))
    tela.blit(texto_recorde, (10, 10))

    pygame.display.update()

# Tela inicial
def tela_inicial(tela):
    rodando = True
    while rodando:
        tela.blit(imagem_background, (0, 0))
        texto = fonte_menu.render("Pressione espaço para jogar", True, (255, 255, 255))
        tela.blit(texto, ((tela_largura - texto.get_width()) // 2, tela_altura // 2))
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    rodando = False

# Tela de Game Over
def tela_game_over(tela, pontos, recorde):
    rodando = True
    while rodando:
        tela.blit(imagem_background, (0, 0))
        texto = fonte_menu.render("Game Over", True, (255, 0, 0))
        texto2 = fonte_menu.render(f"Pontos: {pontos}", True, (255, 255, 255))
        texto3 = fonte_menu.render("Espaço - Jogar | ESC - Sair", True, (255, 255, 255))

        tela.blit(texto, ((tela_largura - texto.get_width()) // 2, 200))
        tela.blit(texto2, ((tela_largura - texto2.get_width()) // 2, 260))
        tela.blit(texto3, ((tela_largura - texto3.get_width()) // 2, 320))
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    rodando = False
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Função principal do jogo
def main():
    pygame.init()
    tela = pygame.display.set_mode((tela_largura, tela_altura))
    pygame.display.set_caption("Flappy Bird - Python")

    try:
        with open("recorde.txt", "r") as arquivo:
            recorde = int(arquivo.read())
    except:
        recorde = 0

    while True:
        tela_inicial(tela)

        passaros = [Passaro(230, 350)]
        canos = [Cano(700)]
        chao = Chao(730)
        pontos = 0

        relogio = pygame.time.Clock()

        rodando = True
        while rodando:
            relogio.tick(30)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        for passaro in passaros:
                            passaro.pular()

            for passaro in passaros:
                passaro.mover()

            chao.mover()

            add_cano = False
            remover_canos = []
            for cano in canos:
                for i, passaro in enumerate(passaros):
                    if cano.colidir(passaro):
                        som_colisao.play()
                        tela_game_over(tela, pontos, recorde)
                        rodando = False
                        break

                    if not cano.passou and passaro.x > cano.x:
                        cano.passou = True
                        add_cano = True

                cano.mover()

                if cano.x + cano.cano_topo.get_width() < 0:
                    remover_canos.append(cano)

            if add_cano:
                pontos += 1
                som_ponto.play()
                canos.append(Cano(600))

            for cano in remover_canos:
                canos.remove(cano)

            for i, passaro in enumerate(passaros):
                if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                    som_colisao.play()
                    tela_game_over(tela, pontos, recorde)
                    rodando = False
                    break

            if pontos > recorde:
                recorde = pontos
                with open("recorde.txt", "w") as arquivo:
                    arquivo.write(str(recorde))

            desenhar_tela(tela, passaros, canos, chao, pontos, recorde)

if __name__ == "__main__":
    main()
