# software projetado por Joao Machado https://github.com/jpfogato
#
# O objetivo do projeto e' ter um veiculo autonomo controlado por visao de maquina,
# com auxilio de rede neural implementada no tensorflow, usando como plataforma o Raspberry Pi
#
# Modulos do software:
# 1 - Setup da aplicacao
# 2 - Aquisicao das imagens
# 3 - Insercao da imagem adquirida em tempo real no algoritimo de detecao (rede neural)
# 4 - Identificacao da acao de comando por imagem
# 5 - Identificacao da acao de comando por distancia
# 6 - Conjuncao booleana (imagem E distancia) para identificacao de acao
# 7 - Execucao da manobra, retorno ao modulo 2
# 8 - Modulos de teste e debugging

# -----------------------------------------------------------------------------
# MODULO 1: SETUP DA APLICACAO
# Neste modulo e feita a:
# importacao das bibliotecas necessarias para a execucao do programa,
# configuracao dos pinos de entrada e saida do Raspberry Pi,
# definicao da compressao da imagem recebida pela camera (HxV pixels)

import Modulos/MOD_01_Setup

# -----------------------------------------------------------------------------
# MODULO 8: TESTES E DEBUGGING
# Na versao final esse modulo deve estar comentado
# Documentar cada parte para aplicacao de debug rapido

# Teste 1: ambos os motores para frente ate que alvo esteja a menos de 10cm
# Remova o comentario das proximas linhas para chamar este modulo

 import Modulos/MOD_08_Teste_01
