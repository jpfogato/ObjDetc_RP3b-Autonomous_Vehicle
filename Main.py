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

#import os
#import cv2
#import numpy as np
#from picamera.array import PiRGBArray
#from picamera import PiCamera
#import tensorflow as tf
#import argparse
import sys #biblioteca de funcoes de sistema
import RPi.GPIO as GPIO #biblioteca de acesso aos pinos do Rasbperry
import time #biblioteca com funcoes de temporizacao

GPIO.setmode(GPIO.BCM) #trabalha com os pinos fisicos atraves da nomenclatura da GPIO

# Pinos do sensor HC-SR04
TRIGGER = 17 #GPIO 17 - PINO 11 - usado como fonte de TRIGGER
ECHO = 4 #GPIO 04 - PINO 07 - usado como recebedor do pulso

# Pinos utilizados pelo MOTOR 1
M1Frente = 25 #GPIO 25 - PINO 22
M1Tras = 24 #GPIO 24 - PINO 18
M1Controle = 23 #GPIO 23 - PINO 16

# Pinos utilizados pelo MOTOR 2
M2Frente = 20 #GPIO 20 - PINO 38
M2Tras = 16 #GPIO 16 - PINO 36
M2Controle = 21 #GPIO 21 - PINO 40 *** PODE SER NECESSARIO ALTERAR - SUGESTAO: GPIO 18 PINO 12

# Setup dos pinos do sensor HC-SR04
GPIO.setup(TRIGGER,GPIO.OUT) #define o pino TRIGGER como SAIDA
GPIO.setup(ECHO,GPIO.IN) #define o pino ECHO como ENTRADA
GPIO.output(TRIGGER,GPIO.LOW) #define a SAIDA do pino TRIGGER como BAIXA

# Setup dos pinos do MOTOR 1
GPIO.setup(M1Frente,GPIO.OUT) #define o pino M1Frente como SAIDA
GPIO.setup(M1Tras,GPIO.OUT) #define o pino M1Tras como SAIDA
GPIO.setup(M1PWM,GPIO.OUT) #define o pino M1PWM como SAIDA
GPIO.output(M1Frente,GPIO.LOW) #define a SAIDA do pino M1Frente como BAIXA
GPIO.output(M1Tras,GPIO.LOW) #define a SAIDA do pino M1Tras como BAIXA
M1pwm=GPIO.PWM(M1Controle,50) #define o pino M1Controle como saida para um PWM de 50Hz

# Setup dos pinos do MOTOR 2
GPIO.setup(M2Frente,GPIO.OUT) #define o pino M2Frente como SAIDA
GPIO.setup(M2Tras,GPIO.OUT) #define o pino M2Tras como SAIDA
GPIO.setup(M2PWM,GPIO.OUT) #define o pino M2PWM como SAIDA
GPIO.output(M2Frente,GPIO.LOW) #define a SAIDA do pino M2Frente como BAIXA
GPIO.output(M2Tras,GPIO.LOW) #define a SAIDA do pino M2Tras como BAIXA
M2pwm=GPIO.PWM(M2Controle,50) #define o pino M2Controle como saida para um PWM de 50Hz

# Inicio do PWM nos motores
M1pwm.start(0) #define o dutycycle inicial no motor 1 em 0%
M2pwm.start(0) #define o dutycycle inicial no motor 2 em 0%

# setup de constantes da camera
#IM_WIDTH = 800 #800 pixels horizontais
#IM_HEIGHT = 600 #600 pixels verticais

# selecao de camera: PiCam
#camera_type = 'picamera'


# -----------------------------------------------------------------------------
# MODULO 8: TESTES E DEBUGGING
# Na versao final esse modulo deve estar comentado
# Documentar cada parte para aplicacao de debug rapido

# Teste 1: ambos os motores para frente ate que alvo esteja a menos de 10cm
# Remova o comentario das proximas linhas para chamar este modulo

 import Modulos/debug8_1
