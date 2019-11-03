import os #biblioteca com funcoes do Linux
import cv2 #biblioteca com funcoes do OpenCV
import numpy as np #biblioteca de funcoes e operadores matematicos
from picamera.array import PiRGBArray #biblioteca com funcoes  de processamento de imagem da PiCam
from picamera import PiCamera #bliblioteca com funcoes da PiCam
import tensorflow as tf #biblioteca com funcoes do TensorFlow
import argparse #
import sys #
import RPi.GPIO as GPIO #biblioteca de acesso aos pinos do Rasbperry
import time #biblioteca com funcoes de temporizacao
#import tensorflow.compat.v1 as tf #tente isso se houver problemas de compatibilidade entre versoes do TF
#tf.disable_v2_behavior()

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
IM_WIDTH = 800 #800 pixels horizontais
IM_HEIGHT = 600 #600 pixels verticais

# adiciona os comandos ao ambiente PATH do Linux
sys.path.append('..')

# Importa utils do algoritimo de deteccao
from utils import label_map_util #funcoes de verificacao de labels
from utils import visualization_utils as vis_util #funcoes de vizualizacao
