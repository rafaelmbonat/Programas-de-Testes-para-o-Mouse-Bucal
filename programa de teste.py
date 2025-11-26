import pygame
import sys
import random
import csv
import os
from datetime import datetime

def posicao_aleatoria():
    """Gera uma posição aleatória que não sobrepõe os botões"""
    while True:
        x = random.randint(0, LARGURA - TAMANHO_QUADRADO)
        y = random.randint(0, ALTURA - TAMANHO_QUADRADO)
        
        # Verifica se a posição não sobrepõe os botões
        if not sobrepoe_botoes(x, y):
            return x, y

def sobrepoe_botoes(x, y):
    """Verifica se a posição (x,y) sobrepõe algum botão"""
    # Área do botão liga/desliga
    botao_liga_rect = pygame.Rect(botao_liga_x, botao_liga_y, LARGURA_BOTAO, ALTURA_BOTAO)
    # Área do botão 30 cliques
    botao_teste_rect = pygame.Rect(botao_teste_x, botao_teste_y, LARGURA_BOTAO, ALTURA_BOTAO)
    # Área do quadrado
    quadrado_rect = pygame.Rect(x, y, TAMANHO_QUADRADO, TAMANHO_QUADRADO)
    
    # Verifica colisão com algum botão
    return quadrado_rect.colliderect(botao_liga_rect) or quadrado_rect.colliderect(botao_teste_rect)

def cor_aleatoria():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def salvar_dados():
    """Salva os dados coletados em um arquivo CSV"""
    if not tempos_cliques:
        return
    
    # Cria pasta de dados se não existir
    if not os.path.exists('dados'):
        os.makedirs('dados')
    
    # Nome do arquivo com timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f'dados/teste_agilidade_{timestamp}.csv'
    
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(['Numero_Clique', 'Tempo_Reacao(s)', 'Timestamp'])
        
        for i, tempo in enumerate(tempos_cliques, 1):
            writer.writerow([i, tempo, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    
    print(f"Dados salvos em: {nome_arquivo}")

def iniciar_teste_30_cliques():
    """Reinicia todas as variáveis para um novo teste de 30 cliques"""
    global contador_cliques, tempo_inicio, tempo_ultimo, soma_tempos, tempos_cliques, teste_concluido
    contador_cliques = 0
    tempo_ultimo = 0.0
    soma_tempos = 0.0
    tempos_cliques = []
    teste_concluido = False
    tempo_inicio = pygame.time.get_ticks()
    quadrado_x, quadrado_y = posicao_aleatoria()
    return quadrado_x, quadrado_y

pygame.init()

LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Teste de Agilidade - 30 Cliques")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 100, 255)
CINZA = (200, 200, 200)
VERDE_CLARO = (100, 255, 100)
VERMELHO_CLARO = (255, 100, 100)
AZUL_CLARO = (100, 200, 255)
AMARELO = (255, 255, 0)

TAMANHO_QUADRADO = 20
LARGURA_BOTAO = 150
ALTURA_BOTAO = 40
ESPACAMENTO_BOTOES = 10

# Variáveis do programa
contador_cliques = 0
tempo_inicio = pygame.time.get_ticks()
tempo_ultimo = 0.0
soma_tempos = 0.0
programa_ligado = False
teste_concluido = False
tempos_cliques = []  # Lista para armazenar todos os tempos de reação

# Posições dos botões
botao_liga_x = LARGURA - LARGURA_BOTAO - 20
botao_liga_y = 20

botao_teste_x = LARGURA - LARGURA_BOTAO - 20
botao_teste_y = botao_liga_y + ALTURA_BOTAO + ESPACAMENTO_BOTOES

# Definir área segura (onde os quadrados podem aparecer)
MARGEM_SEGURANCA = 10  # Margem adicional de segurança
area_segura_x = 0
area_segura_y = 0
area_segura_largura = LARGURA - LARGURA_BOTAO - 20 - MARGEM_SEGURANCA
area_segura_altura = ALTURA

quadrado_x = 100
quadrado_y = 100
cor_quadrado = VERDE

fonte = pygame.font.SysFont(None, 30)
fonte_pequena = pygame.font.SysFont(None, 24)

while True:
    tempo_atual = pygame.time.get_ticks()
    tempo_decorrido = (tempo_atual - tempo_inicio) / 1000

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            # Salva os dados antes de fechar
            if tempos_cliques:
                salvar_dados()
            pygame.quit()
            sys.exit()
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = evento.pos
            
            # Verifica clique no botão liga/desliga
            if (botao_liga_x <= mouse_x <= botao_liga_x + LARGURA_BOTAO) and \
               (botao_liga_y <= mouse_y <= botao_liga_y + ALTURA_BOTAO):
                programa_ligado = not programa_ligado
                if programa_ligado:
                    # Reinicia contadores quando liga
                    quadrado_x, quadrado_y = iniciar_teste_30_cliques()
                else:
                    # Salva dados quando desliga
                    if tempos_cliques:
                        salvar_dados()
            
            # Verifica clique no botão de teste de 30 cliques
            if (botao_teste_x <= mouse_x <= botao_teste_x + LARGURA_BOTAO) and \
               (botao_teste_y <= mouse_y <= botao_teste_y + ALTURA_BOTAO):
                if programa_ligado:
                    quadrado_x, quadrado_y = iniciar_teste_30_cliques()
            
            # Verifica clique no quadrado (apenas se programa estiver ligado e teste não concluído)
            if programa_ligado and not teste_concluido and \
               (quadrado_x <= mouse_x <= quadrado_x + TAMANHO_QUADRADO) and \
               (quadrado_y <= mouse_y <= quadrado_y + TAMANHO_QUADRADO):
                
                tempo_ultimo = tempo_decorrido
                soma_tempos += tempo_ultimo
                tempos_cliques.append(tempo_ultimo)  # Armazena o tempo de reação
                
                contador_cliques += 1
                
                # Verifica se atingiu 30 cliques
                if contador_cliques >= 30:
                    teste_concluido = True
                    # Salva automaticamente ao concluir o teste
                    salvar_dados()
                else:
                    # Move o quadrado apenas se não tiver concluído
                    quadrado_x, quadrado_y = posicao_aleatoria()
                    tempo_inicio = pygame.time.get_ticks()
                    cor_quadrado = cor_aleatoria()

    TELA.fill(BRANCO)

    # Calcula tempo médio
    if contador_cliques > 0:
        tempo_medio = soma_tempos / contador_cliques
    else:
        tempo_medio = 0.0

    # Desenha informações na tela
    texto_contador = fonte.render(f"Cliques: {contador_cliques}/30", True, PRETO)
    texto_tempo_atual = fonte.render(f"Atual: {tempo_decorrido:.2f}s", True, PRETO)
    texto_ultimo = fonte.render(f"Último: {tempo_ultimo:.2f}s", True, PRETO)
    texto_medio = fonte.render(f"Médio: {tempo_medio:.2f}s", True, PRETO)
    
    # Status do programa
    status_texto = "PROGRAMA: LIGADO" if programa_ligado else "PROGRAMA: DESLIGADO"
    status_cor = VERDE if programa_ligado else VERMELHO
    texto_status = fonte.render(status_texto, True, status_cor)
    
    # Status do teste
    if teste_concluido:
        status_teste = "TESTE CONCLUÍDO!"
        cor_teste = AMARELO
    else:
        status_teste = "TESTE EM ANDAMENTO"
        cor_teste = AZUL
    texto_teste = fonte.render(status_teste, True, cor_teste)

    TELA.blit(texto_contador, (10, 10))
    TELA.blit(texto_tempo_atual, (10, 40))
    TELA.blit(texto_ultimo, (10, 70))
    TELA.blit(texto_medio, (10, 100))
    TELA.blit(texto_status, (10, 140))
    TELA.blit(texto_teste, (10, 170))
    
    # Informações sobre coleta de dados
    if tempos_cliques:
        texto_dados = fonte_pequena.render(f"Dados coletados: {len(tempos_cliques)} tempos", True, PRETO)
        TELA.blit(texto_dados, (10, 200))
        
        # Mostra progresso do teste
        progresso = f"Progresso: {contador_cliques}/30 ({contador_cliques/30*100:.0f}%)"
        texto_progresso = fonte_pequena.render(progresso, True, PRETO)
        TELA.blit(texto_progresso, (10, 230))

    # Desenha o quadrado alvo (apenas se programa estiver ligado e teste não concluído)
    if programa_ligado and not teste_concluido:
        pygame.draw.rect(TELA, cor_quadrado, (quadrado_x, quadrado_y, TAMANHO_QUADRADO, TAMANHO_QUADRADO))
    elif programa_ligado and teste_concluido:
        # Mostra quadrado cinza quando teste concluído
        pygame.draw.rect(TELA, CINZA, (quadrado_x, quadrado_y, TAMANHO_QUADRADO, TAMANHO_QUADRADO))
    else:
        # Mostra quadrado cinza quando desligado
        pygame.draw.rect(TELA, CINZA, (quadrado_x, quadrado_y, TAMANHO_QUADRADO, TAMANHO_QUADRADO))

    # Desenha botão liga/desliga
    cor_botao_liga = VERDE_CLARO if programa_ligado else VERMELHO_CLARO
    pygame.draw.rect(TELA, cor_botao_liga, (botao_liga_x, botao_liga_y, LARGURA_BOTAO, ALTURA_BOTAO))
    pygame.draw.rect(TELA, PRETO, (botao_liga_x, botao_liga_y, LARGURA_BOTAO, ALTURA_BOTAO), 2)
    
    texto_botao_liga = fonte.render("LIGAR/DESLIGAR", True, PRETO)
    texto_botao_liga_rect = texto_botao_liga.get_rect(center=(botao_liga_x + LARGURA_BOTAO//2, botao_liga_y + ALTURA_BOTAO//2))
    TELA.blit(texto_botao_liga, texto_botao_liga_rect)

    # Desenha botão de teste de 30 cliques
    cor_botao_teste = AZUL_CLARO if programa_ligado and not teste_concluido else CINZA
    pygame.draw.rect(TELA, cor_botao_teste, (botao_teste_x, botao_teste_y, LARGURA_BOTAO, ALTURA_BOTAO))
    pygame.draw.rect(TELA, PRETO, (botao_teste_x, botao_teste_y, LARGURA_BOTAO, ALTURA_BOTAO), 2)
    
    texto_botao_teste = fonte.render("INICIAR 30 CLIQUES", True, PRETO)
    texto_botao_teste_rect = texto_botao_teste.get_rect(center=(botao_teste_x + LARGURA_BOTAO//2, botao_teste_y + ALTURA_BOTAO//2))
    TELA.blit(texto_botao_teste, texto_botao_teste_rect)

    # (Opcional) Desenhar área segura para debug - remova estas linhas na versão final
    # pygame.draw.rect(TELA, (200, 200, 200, 50), (area_segura_x, area_segura_y, area_segura_largura, area_segura_altura), 1)

    pygame.display.update()