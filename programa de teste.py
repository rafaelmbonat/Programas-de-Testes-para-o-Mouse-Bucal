import pygame
import sys
import random
import csv
import os
from datetime import datetime

# Constantes de tamanho dos quadrados
PEQUENO = 15
MEDIO = 25
GRANDE = 35
TAMANHOS_QUADRADO = [PEQUENO, MEDIO, GRANDE]
NOMES_TAMANHOS = {PEQUENO: "Pequeno", MEDIO: "Médio", GRANDE: "Grande"}

def posicao_aleatoria(tamanho_quadrado):
    """Gera uma posição aleatória que não sobrepõe os botões"""
    while True:
        x = random.randint(0, LARGURA - tamanho_quadrado)
        y = random.randint(0, ALTURA - tamanho_quadrado)
        
        # Verifica se a posição não sobrepõe os botões
        if not sobrepoe_botoes(x, y, tamanho_quadrado):
            return x, y

def sobrepoe_botoes(x, y, tamanho_quadrado):
    """Verifica se a posição (x,y) sobrepõe algum botão"""
    # Área do botão liga/desliga
    botao_liga_rect = pygame.Rect(botao_liga_x, botao_liga_y, LARGURA_BOTAO, ALTURA_BOTAO)
    # Área do botão 30 cliques
    botao_teste_rect = pygame.Rect(botao_teste_x, botao_teste_y, LARGURA_BOTAO, ALTURA_BOTAO)
    # Área do quadrado
    quadrado_rect = pygame.Rect(x, y, tamanho_quadrado, tamanho_quadrado)
    
    # Verifica colisão com algum botão
    return quadrado_rect.colliderect(botao_liga_rect) or quadrado_rect.colliderect(botao_teste_rect)

def cor_aleatoria():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def obter_tamanho_aleatorio():
    """Retorna um tamanho aleatório para o quadrado"""
    return random.choice(TAMANHOS_QUADRADO)

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
        writer.writerow(['Numero_Clique', 'Tempo_Reacao(s)', 'Tamanho_Alvo', 'Timestamp'])
        
        for i, (tempo, tamanho) in enumerate(zip(tempos_cliques, tamanhos_cliques), 1):
            writer.writerow([i, tempo, NOMES_TAMANHOS[tamanho], datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    
    print(f"Dados salvos em: {nome_arquivo}")

def iniciar_teste_30_cliques():
    """Reinicia todas as variáveis para um novo teste de 30 cliques"""
    global contador_cliques, tempo_inicio, tempo_ultimo, soma_tempos, tempos_cliques, teste_concluido
    global cliques_errados, tamanhos_cliques, tamanho_atual
    contador_cliques = 0
    tempo_ultimo = 0.0
    soma_tempos = 0.0
    tempos_cliques = []
    tamanhos_cliques = []
    cliques_errados = 0
    teste_concluido = False
    tempo_inicio = pygame.time.get_ticks()
    tamanho_atual = obter_tamanho_aleatorio()
    quadrado_x, quadrado_y = posicao_aleatoria(tamanho_atual)
    return quadrado_x, quadrado_y

pygame.init()

LARGURA = 800
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Teste de Agilidade - 30 Cliques com Dificuldade Variável")

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
LARANJA = (255, 165, 0)

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
cliques_errados = 0
tempos_cliques = []  # Lista para armazenar todos os tempos de reação
tamanhos_cliques = []  # Lista para armazenar os tamanhos de cada clique
tamanho_atual = MEDIO  # Tamanho inicial do quadrado

# Posições dos botões
botao_liga_x = LARGURA - LARGURA_BOTAO - 20
botao_liga_y = 20

botao_teste_x = LARGURA - LARGURA_BOTAO - 20
botao_teste_y = botao_liga_y + ALTURA_BOTAO + ESPACAMENTO_BOTOES

quadrado_x = 100
quadrado_y = 100
cor_quadrado = VERDE

fonte = pygame.font.SysFont(None, 30)
fonte_pequena = pygame.font.SysFont(None, 24)
fonte_grande = pygame.font.SysFont(None, 36)

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
            elif (botao_teste_x <= mouse_x <= botao_teste_x + LARGURA_BOTAO) and \
                 (botao_teste_y <= mouse_y <= botao_teste_y + ALTURA_BOTAO):
                if programa_ligado:
                    quadrado_x, quadrado_y = iniciar_teste_30_cliques()
            
            # Verifica clique no quadrado (apenas se programa estiver ligado e teste não concluído)
            elif programa_ligado and not teste_concluido:
                # Verifica se acertou o quadrado
                if (quadrado_x <= mouse_x <= quadrado_x + tamanho_atual) and \
                   (quadrado_y <= mouse_y <= quadrado_y + tamanho_atual):
                    
                    tempo_ultimo = tempo_decorrido
                    soma_tempos += tempo_ultimo
                    tempos_cliques.append(tempo_ultimo)  # Armazena o tempo de reação
                    tamanhos_cliques.append(tamanho_atual)  # Armazena o tamanho do alvo
                    
                    contador_cliques += 1
                    
                    # Verifica se atingiu 30 cliques
                    if contador_cliques >= 30:
                        teste_concluido = True
                        # Salva automaticamente ao concluir o teste
                        salvar_dados()
                    else:
                        # Move o quadrado apenas se não tiver concluído
                        tamanho_atual = obter_tamanho_aleatorio()
                        quadrado_x, quadrado_y = posicao_aleatoria(tamanho_atual)
                        tempo_inicio = pygame.time.get_ticks()
                        cor_quadrado = cor_aleatoria()
                
                else:
                    # Clique fora do quadrado - conta como erro
                    cliques_errados += 1

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
    texto_errados = fonte.render(f"Erros: {cliques_errados}", True, VERMELHO)
    
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
    
    # Informações do tamanho atual
    if programa_ligado and not teste_concluido:
        tamanho_texto = f"Tamanho: {NOMES_TAMANHOS[tamanho_atual]}"
        texto_tamanho = fonte.render(tamanho_texto, True, LARANJA)
    else:
        texto_tamanho = fonte.render("Tamanho: -", True, LARANJA)

    TELA.blit(texto_contador, (10, 10))
    TELA.blit(texto_tempo_atual, (10, 40))
    TELA.blit(texto_ultimo, (10, 70))
    TELA.blit(texto_medio, (10, 100))
    TELA.blit(texto_errados, (10, 130))
    TELA.blit(texto_status, (10, 160))
    TELA.blit(texto_teste, (10, 190))
    TELA.blit(texto_tamanho, (10, 220))
    
    # Informações sobre coleta de dados
    if tempos_cliques:
        texto_dados = fonte_pequena.render(f"Dados coletados: {len(tempos_cliques)} tempos", True, PRETO)
        TELA.blit(texto_dados, (10, 250))
        
        # Mostra progresso do teste
        progresso = f"Progresso: {contador_cliques}/30 ({contador_cliques/30*100:.0f}%)"
        texto_progresso = fonte_pequena.render(progresso, True, PRETO)
        TELA.blit(texto_progresso, (10, 280))
        
        # Mostra precisão
        if contador_cliques + cliques_errados > 0:
            precisao = (contador_cliques / (contador_cliques + cliques_errados)) * 100
            texto_precisao = fonte_pequena.render(f"Precisão: {precisao:.1f}%", True, PRETO)
            TELA.blit(texto_precisao, (10, 310))

    # Desenha o quadrado alvo (apenas se programa estiver ligado e teste não concluído)
    if programa_ligado and not teste_concluido:
        pygame.draw.rect(TELA, cor_quadrado, (quadrado_x, quadrado_y, tamanho_atual, tamanho_atual))
        
        # (Opcional) Desenha borda para melhor visualização
        pygame.draw.rect(TELA, PRETO, (quadrado_x, quadrado_y, tamanho_atual, tamanho_atual), 2)
    elif programa_ligado and teste_concluido:
        # Mostra quadrado cinza quando teste concluído
        pygame.draw.rect(TELA, CINZA, (quadrado_x, quadrado_y, tamanho_atual, tamanho_atual))
    else:
        # Mostra quadrado cinza quando desligado
        pygame.draw.rect(TELA, CINZA, (quadrado_x, quadrado_y, tamanho_atual, tamanho_atual))

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

    pygame.display.update()
