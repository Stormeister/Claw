import pygame
import random
import math
import sys


pygame.init()

# tela
LARGURA = 1060
ALTURA = 810
FPS = 60

# Cor
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 100, 200)
VERDE = (0, 200, 0)
VERMELHO = (200, 0, 0)
AMARELO = (255, 255, 0)
ROXO = (150, 0, 150)
LARANJA = (255, 165, 0)
AZUL_CLARO = (173, 216, 230)
VERDE_CLARO = (144, 238, 144)

class projeto:
    def __init__(self):
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Jogos Olímpicos")
        self.relogio = pygame.time.Clock()
        self.fonte_grande = pygame.font.Font(None, 48)
        self.fonte_media = pygame.font.Font(None, 36)
        self.fonte_pequena = pygame.font.Font(None, 24)
        
        self.estado = "menu"  # menu, corrida, malabarismo, ping_pong, resultados, parabens
        self.pontuacao_total = 0
        self.jogos_completados = []
        self.jogo_anterior = ""  # Para saber de qual jogo veio
        
        # Variáveis do jogador
        self.jogador_x = LARGURA // 2
        self.jogador_y = ALTURA // 2
        self.velocidade_jogador = 5
        
    def desenhar_menu(self):
        self.tela.fill(AZUL_CLARO)
        
        # Título
        titulo = self.fonte_grande.render("projeto", True, PRETO)
        titulo_rect = titulo.get_rect(center=(LARGURA//2, 100))
        self.tela.blit(titulo, titulo_rect)
        
        subtitulo = self.fonte_media.render("Escolha seu esporte!", True, PRETO)
        subtitulo_rect = subtitulo.get_rect(center=(LARGURA//2, 150))
        self.tela.blit(subtitulo, subtitulo_rect)
        
        opcoes = [
            ("1 -  CORRIDA ", 250),
            ("2 -  MALABARISMO", 300),
            ("3 -  PING PONG", 350),
            ("4 -  VER RESULTADOS", 400),
            ("ESC - SAIR", 500)
        ]
        
        for opcao, y in opcoes:
            texto = self.fonte_media.render(opcao, True, PRETO)
            texto_rect = texto.get_rect(center=(LARGURA//2, y))
            self.tela.blit(texto, texto_rect)
        
        # Pontuação 
        pontos_texto = self.fonte_media.render(f"Pontuação Total: {self.pontuacao_total}", True, ROXO)
        pontos_rect = pontos_texto.get_rect(center=(LARGURA//2, 550))
        self.tela.blit(pontos_texto, pontos_rect)

    def jogo_corrida(self):
        if not hasattr(self, 'corrida_iniciada'):
            self.corrida_iniciada = True
            self.posicao_jogador = 0
            self.velocidade_corrida = 0
            self.tempo_corrida = 0
            self.meta = 2400  # 300m 
            self.teclas_pressionadas = []
            self.ultimo_tempo_tecla = 0
            
        self.tela.fill(VERDE_CLARO)
        
        # Desenhar pista 
        pygame.draw.rect(self.tela, VERDE, (50, 300, 900, 200))
        for i in range(0, 900, 100):
            pygame.draw.line(self.tela, BRANCO, (50 + i, 350), (50 + i + 50, 350), 3)
        
        # Linha de largada e chegada
        pygame.draw.line(self.tela, PRETO, (100, 300), (100, 500), 5)
        pygame.draw.line(self.tela, VERMELHO, (850, 300), (850, 500), 5)
        
        # posição do jogador
        keys = pygame.key.get_pressed()
        tempo_atual = pygame.time.get_ticks()
        
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            if tempo_atual - self.ultimo_tempo_tecla > 200:
                self.velocidade_corrida += 3
                self.ultimo_tempo_tecla = tempo_atual
        
        # Diminuir velocidade gradualmente
        self.velocidade_corrida *= 0.98
        self.posicao_jogador += self.velocidade_corrida
        
        # Desenhar corredor (posição relativa para 300m)
        progresso = min(self.posicao_jogador / self.meta, 1.0)
        jogador_x = 100 + progresso * 750
        pygame.draw.circle(self.tela, AZUL, (int(jogador_x), 400), 20)
        pygame.draw.rect(self.tela, VERMELHO, (int(jogador_x-10), 380, 20, 40))
        
        # Tempo
        self.tempo_corrida += 1/FPS
        tempo_texto = self.fonte_media.render(f"Tempo: {self.tempo_corrida:.2f}s", True, PRETO)
        self.tela.blit(tempo_texto, (50, 50))
        
        distancia_texto = self.fonte_pequena.render(f"Distância: {int(progresso * 300)}m / 300m", True, PRETO)
        self.tela.blit(distancia_texto, (50, 80))
        
        # Instruções
        instrucao = self.fonte_pequena.render("Pressione ESQUERDA e DIREITA alternadamente para correr!", True, PRETO)
        self.tela.blit(instrucao, (50, 110))
        
        velocidade_texto = self.fonte_pequena.render(f"Velocidade: {self.velocidade_corrida:.1f}", True, PRETO)
        self.tela.blit(velocidade_texto, (50, 140))
        
        # Verificar se chegou na meta
        if self.posicao_jogador >= self.meta:
            pontos = max(0, 1500 - int(self.tempo_corrida * 30))  # Ajustado para 300m
            self.pontuacao_total += pontos
            if "corrida" not in self.jogos_completados:
                self.jogos_completados.append("corrida")
            
            self.jogo_anterior = "corrida"
            self.pontos_jogo_anterior = pontos
            self.tempo_jogo_anterior = self.tempo_corrida
            self.estado = "parabens"
            
    def jogo_malabarismo(self):
        if not hasattr(self, 'malabarismo_iniciado'):
            self.malabarismo_iniciado = True
            self.bolas = []
            self.tempo_malabarismo = 0
            self.pontos_malabarismo = 0
            self.bolas_no_ar = 0
            self.combo = 0
            self.max_combo = 0
            
            # Criar bolas iniciais
            for i in range(3):
                self.bolas.append({
                    'x': LARGURA//2 + i * 50 - 50,
                    'y': ALTURA - 100,
                    'vel_x': 0,
                    'vel_y': 0,
                    'no_ar': False,
                    'cor': [VERMELHO, AZUL, AMARELO][i]
                })
            
        self.tela.fill(AZUL_CLARO)
        
        # Desenhar palco
        pygame.draw.rect(self.tela, VERDE_CLARO, (0, ALTURA-150, LARGURA, 150))
        
        # Controles
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        # Atualizar bolas
        for bola in self.bolas:
            if bola['no_ar']:
                bola['x'] += bola['vel_x']
                bola['y'] += bola['vel_y']
                bola['vel_y'] += 0.5  # Gravidade
                
                # Verificar se caiu no chão
                if bola['y'] >= ALTURA - 120:
                    bola['y'] = ALTURA - 120
                    bola['no_ar'] = False
                    bola['vel_x'] = 0
                    bola['vel_y'] = 0
                    self.combo = 0  # Quebra combo se cair
            
            # Desenhar bola
            pygame.draw.circle(self.tela, bola['cor'], (int(bola['x']), int(bola['y'])), 15)
            
            # Verificar clique na bola
            if pygame.mouse.get_pressed()[0]:
                dist = math.sqrt((mouse_pos[0] - bola['x'])**2 + (mouse_pos[1] - bola['y'])**2)
                if dist < 20 and not bola['no_ar']:
                    # Lançar bola
                    bola['vel_x'] = (mouse_pos[0] - bola['x']) * 0.1
                    bola['vel_y'] = -15 - random.randint(0, 5)
                    bola['no_ar'] = True
                    self.combo += 1
                    self.max_combo = max(self.max_combo, self.combo)
                    self.pontos_malabarismo += 10 * self.combo
        
        # Contar bolas no ar
        self.bolas_no_ar = sum(1 for bola in self.bolas if bola['no_ar'])
        
        # Tempo
        self.tempo_malabarismo += 1/FPS
        
        # Interface
        tempo_texto = self.fonte_media.render(f"Tempo: {self.tempo_malabarismo:.1f}s", True, PRETO)
        self.tela.blit(tempo_texto, (50, 50))
        
        pontos_texto = self.fonte_media.render(f"Pontos: {self.pontos_malabarismo}", True, PRETO)
        self.tela.blit(pontos_texto, (50, 100))
        
        combo_texto = self.fonte_pequena.render(f"Combo: {self.combo} (Máximo: {self.max_combo})", True, PRETO)
        self.tela.blit(combo_texto, (50, 150))
        
        bolas_ar_texto = self.fonte_pequena.render(f"Bolas no ar: {self.bolas_no_ar}", True, PRETO)
        self.tela.blit(bolas_ar_texto, (50, 180))
        
        instrucoes = [
            "Clique nas bolas para lançá-las",
            "Mantenha as bolas no ar para fazer combo",
            "Quanto mais combo, mais pontos!"
        ]
        
        for i, instrucao in enumerate(instrucoes):
            texto = self.fonte_pequena.render(instrucao, True, PRETO)
            self.tela.blit(texto, (50, 220 + i * 25))
        
        # terminar o jogo após 60 segundos
        if self.tempo_malabarismo >= 60:
            self.pontuacao_total += self.pontos_malabarismo
            if "malabarismo" not in self.jogos_completados:
                self.jogos_completados.append("malabarismo")
            
            self.jogo_anterior = "malabarismo"
            self.pontos_jogo_anterior = self.pontos_malabarismo
            self.tempo_jogo_anterior = self.tempo_malabarismo
            self.estado = "parabens"

    def jogo_ping_pong(self):
        if not hasattr(self, 'ping_pong_iniciado'):
            self.ping_pong_iniciado = True
            self.raquete_jogador_y = ALTURA // 2
            self.raquete_ia_y = ALTURA // 2
            self.bola_x = LARGURA // 2
            self.bola_y = ALTURA // 2
            self.bola_vel_x = 5
            self.bola_vel_y = random.choice([-3, 3])
            self.pontos_jogador = 0
            self.pontos_ia = 0
            self.tempo_ping_pong = 0
            
        self.tela.fill(VERDE)
        
        # Desenhar mesa
        pygame.draw.rect(self.tela, VERDE_CLARO, (100, 200, 800, 300))
        pygame.draw.line(self.tela, BRANCO, (LARGURA//2, 200), (LARGURA//2, 500), 3)
        
        # Controles do jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.raquete_jogador_y > 200:
            self.raquete_jogador_y -= 8
        if keys[pygame.K_DOWN] and self.raquete_jogador_y < 450:
            self.raquete_jogador_y += 8
        
        # IA simples
        if self.bola_y < self.raquete_ia_y - 10:
            self.raquete_ia_y -= 4
        elif self.bola_y > self.raquete_ia_y + 10:
            self.raquete_ia_y += 4
        
        # Atualizar bola
        self.bola_x += self.bola_vel_x
        self.bola_y += self.bola_vel_y
        
        # Colisão com bordas superior e inferior
        if self.bola_y <= 200 or self.bola_y >= 500:
            self.bola_vel_y = -self.bola_vel_y
        
        # Colisão com raquete do jogador
        if (self.bola_x <= 120 and self.bola_x >= 100 and 
            self.bola_y >= self.raquete_jogador_y - 50 and 
            self.bola_y <= self.raquete_jogador_y + 50):
            self.bola_vel_x = abs(self.bola_vel_x)
            self.bola_vel_y += random.randint(-2, 2)
        
        # Colisão com raquete da IA
        if (self.bola_x >= 780 and self.bola_x <= 800 and 
            self.bola_y >= self.raquete_ia_y - 50 and 
            self.bola_y <= self.raquete_ia_y + 50):
            self.bola_vel_x = -abs(self.bola_vel_x)
            self.bola_vel_y += random.randint(-2, 2)
        
        # Pontuação
        if self.bola_x < 50:
            self.pontos_ia += 1
            self.bola_x = LARGURA // 2
            self.bola_y = ALTURA // 2
            self.bola_vel_x = 5
            self.bola_vel_y = random.choice([-3, 3])
        elif self.bola_x > LARGURA - 50:
            self.pontos_jogador += 1
            self.bola_x = LARGURA // 2
            self.bola_y = ALTURA // 2
            self.bola_vel_x = -5
            self.bola_vel_y = random.choice([-3, 3])
        
        # Desenhar elementos
        # Raquete do jogador
        pygame.draw.rect(self.tela, AZUL, (100, self.raquete_jogador_y - 50, 20, 100))
        # Raquete da IA
        pygame.draw.rect(self.tela, VERMELHO, (780, self.raquete_ia_y - 50, 20, 100))
        # Bola
        pygame.draw.circle(self.tela, BRANCO, (int(self.bola_x), int(self.bola_y)), 8)
        
        # Tempo
        self.tempo_ping_pong += 1/FPS
        
        # Interface
        placar = self.fonte_grande.render(f"{self.pontos_jogador} - {self.pontos_ia}", True, BRANCO)
        placar_rect = placar.get_rect(center=(LARGURA//2, 100))
        self.tela.blit(placar, placar_rect)
        
        tempo_texto = self.fonte_media.render(f"Tempo: {self.tempo_ping_pong:.1f}s", True, BRANCO)
        self.tela.blit(tempo_texto, (50, 50))
        
        instrucoes = [
            "Use SETAS para mover sua raquete",
            "Primeiro a fazer 5 pontos ganha!"
        ]
        
        for i, instrucao in enumerate(instrucoes):
            texto = self.fonte_pequena.render(instrucao, True, BRANCO)
            self.tela.blit(texto, (50, 550 + i * 25))
        
        # Verificar fim do jogo
        if self.pontos_jogador >= 5 or self.pontos_ia >= 5:
            pontos_finais = self.pontos_jogador * 100
            self.pontuacao_total += pontos_finais
            if "ping_pong" not in self.jogos_completados:
                self.jogos_completados.append("ping_pong")
            
            self.jogo_anterior = "ping_pong"
            self.pontos_jogo_anterior = pontos_finais
            self.tempo_jogo_anterior = self.tempo_ping_pong
            self.estado = "parabens"

    def tela_parabens(self):
        # tela 
        tela_parabens = pygame.Surface((500, 500))
        tela_parabens.fill(AMARELO)
        
        # Desenhar borda
        pygame.draw.rect(tela_parabens, PRETO, (0, 0, 500, 500), 5)
        
        # Texto de parabéns
        fonte_parabens = pygame.font.Font(None, 48)
        texto_parabens = fonte_parabens.render("PARABÉNS", True, PRETO)
        texto_rect = texto_parabens.get_rect(center=(250, 150))
        tela_parabens.blit(texto_parabens, texto_rect)
        
        texto_vitoria = fonte_parabens.render("PELA SUA", True, PRETO)
        texto_rect2 = texto_vitoria.get_rect(center=(250, 200))
        tela_parabens.blit(texto_vitoria, texto_rect2)
        
        texto_vitoria2 = fonte_parabens.render("VITÓRIA!", True, PRETO)
        texto_rect3 = texto_vitoria2.get_rect(center=(250, 250))
        tela_parabens.blit(texto_vitoria2, texto_rect3)
        
        # Informações do jogo
        nome_jogo = {
            "corrida": "Corrida 300m",
            "malabarismo": "Malabarismo", 
            "ping_pong": "Ping Pong"
        }.get(self.jogo_anterior, "Jogo")
        
        info_jogo = self.fonte_media.render(f"Jogo: {nome_jogo}", True, PRETO)
        info_rect = info_jogo.get_rect(center=(250, 320))
        tela_parabens.blit(info_jogo, info_rect)
        
        info_pontos = self.fonte_media.render(f"Pontos: {self.pontos_jogo_anterior}", True, PRETO)
        info_pontos_rect = info_pontos.get_rect(center=(250, 350))
        tela_parabens.blit(info_pontos, info_pontos_rect)
        
        # Instrução para continuar
        continuar = self.fonte_pequena.render("Pressione ENTER para continuar", True, PRETO)
        continuar_rect = continuar.get_rect(center=(250, 420))
        tela_parabens.blit(continuar, continuar_rect)
        
        # Centralizar na tela principal
        x_pos = (LARGURA - 500) // 2
        y_pos = (ALTURA - 500) // 2
        self.tela.blit(tela_parabens, (x_pos, y_pos))

    def mostrar_resultados(self):
        self.tela.fill(ROXO)
        
        titulo = self.fonte_grande.render("🏆 RESULTADOS FINAIS 🏆", True, BRANCO)
        titulo_rect = titulo.get_rect(center=(LARGURA//2, 100))
        self.tela.blit(titulo, titulo_rect)
        
        pontuacao = self.fonte_media.render(f"Pontuação Total: {self.pontuacao_total}", True, AMARELO)
        pontuacao_rect = pontuacao.get_rect(center=(LARGURA//2, 200))
        self.tela.blit(pontuacao, pontuacao_rect)
        
        jogos_texto = self.fonte_media.render(f"Jogos Completados: {len(self.jogos_completados)}/3", True, BRANCO)
        jogos_rect = jogos_texto.get_rect(center=(LARGURA//2, 250))
        self.tela.blit(jogos_texto, jogos_rect)
        
        # pontuação
        if len(self.jogos_completados) == 3:
            if self.pontuacao_total > 2500:
                medalha = "🥇 MEDALHA DE OURO!"
            elif self.pontuacao_total > 1500:
                medalha = "🥈 MEDALHA DE PRATA!"
            else:
                medalha = "🥉 MEDALHA DE BRONZE!"
            
            medalha_texto = self.fonte_grande.render(medalha, True, AMARELO)
            medalha_rect = medalha_texto.get_rect(center=(LARGURA//2, 350))
            self.tela.blit(medalha_texto, medalha_rect)
        
        y_pos = 400
        for jogo in self.jogos_completados:
            nome_jogo = {
                "corrida": " Corrida dos 300m",
                "malabarismo": " Malabarismo",
                "ping_pong": " Ping Pong"
            }.get(jogo, jogo)
            
            jogo_texto = self.fonte_media.render(nome_jogo, True, VERDE_CLARO)
            jogo_rect = jogo_texto.get_rect(center=(LARGURA//2, y_pos))
            self.tela.blit(jogo_texto, jogo_rect)
            y_pos += 40
        
        voltar = self.fonte_media.render("Pressione ENTER para voltar ao menu", True, BRANCO)
        voltar_rect = voltar.get_rect(center=(LARGURA//2, 600))
        self.tela.blit(voltar, voltar_rect)
    
    def executar(self):
        rodando = True
        
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        if self.estado == "menu":
                            rodando = False
                        else:
                            self.estado = "menu"
                            # Resetar variáveis dos jogos
                            if hasattr(self, 'corrida_iniciada'):
                                delattr(self, 'corrida_iniciada')
                            if hasattr(self, 'malabarismo_iniciado'):
                                delattr(self, 'malabarismo_iniciado')
                            if hasattr(self, 'ping_pong_iniciado'):
                                delattr(self, 'ping_pong_iniciado')
                    
                    elif self.estado == "menu":
                        if evento.key == pygame.K_1:
                            self.estado = "corrida"
                        elif evento.key == pygame.K_2:
                            self.estado = "malabarismo"
                        elif evento.key == pygame.K_3:
                            self.estado = "ping_pong"
                        elif evento.key == pygame.K_4:
                            self.estado = "resultados"
                    
                    elif evento.key == pygame.K_RETURN:
                        if self.estado in ["corrida", "malabarismo", "ping_pong", "resultados", "parabens"]:
                            self.estado = "menu"
                            # Resetar variáveis dos jogos
                            if hasattr(self, 'corrida_iniciada'):
                                delattr(self, 'corrida_iniciada')
                            if hasattr(self, 'malabarismo_iniciado'):
                                delattr(self, 'malabarismo_iniciado')
                            if hasattr(self, 'ping_pong_iniciado'):
                                delattr(self, 'ping_pong_iniciado')
            
            if self.estado == "menu":
                self.desenhar_menu()
            elif self.estado == "corrida":
                self.jogo_corrida()
            elif self.estado == "malabarismo":
                self.jogo_malabarismo()
            elif self.estado == "ping_pong":
                self.jogo_ping_pong()
            elif self.estado == "parabens":
                self.tela.fill(AZUL_CLARO)  # Fundo para a tela de parabéns
                self.tela_parabens()
            elif self.estado == "resultados":
                self.mostrar_resultados()
            
            pygame.display.flip()
            self.relogio.tick(FPS)
        
        pygame.quit()
        sys.exit()

# executar jogo
if __name__ == "__main__":
    print("Iniciando Doodle Champion Island Games!")
    print("Prepare-se para os Jogos Olímpicos!")
    
    jogo = projeto()
    jogo.executar()
