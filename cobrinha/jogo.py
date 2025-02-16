import pygame
import random
from pygame.locals import *

# Configurações da janela
WINDOWS_WIDTH = 600
WINDOWS_HEIGHT = 600
BLOCK = 10  # Tamanho da cobra e dos obstáculos
INICIAL_VELOCIDADE = 10
AUMENTO_VELOCIDADE = 2
PONTOS_PARA_AUMENTAR_VELOCIDADE = 5  # A cada 5 pontos a velocidade aumenta

pygame.font.init()
fonte = pygame.font.SysFont('Arial', 35, True, True)  # Fonte para o texto em negrito e itálico

# Função para verificar se a cobra saiu da tela
def verifica_margens(pos):
    if 0 <= pos['x'] < WINDOWS_WIDTH and 0 <= pos['y'] < WINDOWS_HEIGHT:
        return False
    else:
        return True

# Função de fim de jogo
def game_over():
    mensagem_game_over = "GAME OVER"
    texto_game_over = fonte.render(mensagem_game_over, True, (255, 255, 255))  # Cor vermelha para a mensagem

    # Calcula a posição central
    texto_largura = texto_game_over.get_width()
    texto_altura = texto_game_over.get_height()

    pos_x = (WINDOWS_WIDTH - texto_largura) // 2
    pos_y = (WINDOWS_HEIGHT - texto_altura) // 2

    # Exibe a mensagem de Game Over
    window.fill((0, 0, 0))  # Preenche o fundo de preto
    window.blit(texto_game_over, (pos_x, pos_y))  # Desenha a mensagem centralizada
    pygame.display.update()

    pygame.time.wait(2000)  # Espera 2 segundos antes de fechar o jogo
    pygame.quit()
    quit()

# Função para gerar comida
def gerar_comida():
    return {'x': random.randint(0, (WINDOWS_WIDTH - BLOCK) // BLOCK) * BLOCK,
            'y': random.randint(0, (WINDOWS_HEIGHT - BLOCK) // BLOCK) * BLOCK}

# Função para gerar obstáculos
def gerar_obstaculo():
    return {'x': random.randint(0, (WINDOWS_WIDTH - BLOCK) // BLOCK) * BLOCK,
            'y': random.randint(0, (WINDOWS_HEIGHT - BLOCK) // BLOCK) * BLOCK}

# Inicializa o pygame
pygame.init()
window = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
pygame.display.set_caption("Jogo da Cobrinha")

# Criando a cobra
cobra_pos = [{'x': WINDOWS_WIDTH // 2, 'y': WINDOWS_HEIGHT // 2}]
cobra_surface = pygame.Surface((BLOCK, BLOCK))
cobra_surface.fill((53, 59, 56))  # Cor da cobra
direcao = K_LEFT  # Direção inicial

# Inicializando o jogo
comida = gerar_comida()
obstaculos = []
velocidade = INICIAL_VELOCIDADE
pontos = 0  # Pontuação inicial
clock = pygame.time.Clock()

# Loop principal do jogo
running = True
while running:
    clock.tick(velocidade)  # Controla a velocidade do jogo
    window.fill((68, 189, 50))  # Cor de fundo

    mensagem = f'Pontos: {pontos}'  # Mensagem de pontuação
    texto = fonte.render(mensagem, True, (255, 255, 255))  # Renderiza o texto

    # Captura eventos do teclado
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False
            pygame.quit()
            quit()
        
        elif evento.type == KEYDOWN:
            if evento.key in [K_RIGHT, K_LEFT, K_UP, K_DOWN]:
                direcao = evento.key  # Atualiza a direção apenas se for válida

    # Atualiza a posição da cobra
    if direcao == K_RIGHT:
        cobra_pos.insert(0, {'x': cobra_pos[0]['x'] + BLOCK, 'y': cobra_pos[0]['y']})
    elif direcao == K_LEFT:
        cobra_pos.insert(0, {'x': cobra_pos[0]['x'] - BLOCK, 'y': cobra_pos[0]['y']})
    elif direcao == K_UP:
        cobra_pos.insert(0, {'x': cobra_pos[0]['x'], 'y': cobra_pos[0]['y'] - BLOCK})
    elif direcao == K_DOWN:
        cobra_pos.insert(0, {'x': cobra_pos[0]['x'], 'y': cobra_pos[0]['y'] + BLOCK})

    # Verifica colisão com as bordas
    if verifica_margens(cobra_pos[0]):
        game_over()

    # Verifica colisão com obstáculos
    for obstaculo in obstaculos:
        if cobra_pos[0]['x'] == obstaculo['x'] and cobra_pos[0]['y'] == obstaculo['y']:
            game_over()

    # Verifica se a cobra comeu a comida
    if cobra_pos[0]['x'] == comida['x'] and cobra_pos[0]['y'] == comida['y']:
        pontos += 1  # Aumenta a pontuação
        comida = gerar_comida()  # Nova comida

        # A cada 5 pontos, aumenta a velocidade
        if pontos % PONTOS_PARA_AUMENTAR_VELOCIDADE == 0:
            velocidade += AUMENTO_VELOCIDADE

        # Adiciona um novo obstáculo
        obstaculos.append(gerar_obstaculo())
    else:
        cobra_pos.pop()  # Remove a última parte da cobra (cauda)

    # Desenha a cobra
    for pos in cobra_pos:
        window.blit(cobra_surface, (pos['x'], pos['y']))

    # Desenha a comida
    pygame.draw.rect(window, (255, 0, 0), (comida['x'], comida['y'], BLOCK, BLOCK))

    # Desenha os obstáculos
    for obstaculo in obstaculos:
        pygame.draw.rect(window, (0, 0, 0), (obstaculo['x'], obstaculo['y'], BLOCK, BLOCK))

    window.blit(texto, (420, 30))  # Desenha a pontuação
    pygame.display.update()  # Atualiza a tela