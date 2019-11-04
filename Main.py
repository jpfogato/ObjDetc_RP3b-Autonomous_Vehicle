# software disponivel em github.com/jpfogato
#
# O objetivo do projeto e' ter um veiculo autonomo controlado por visao de
# maquina, com auxilio de rede neural implementada no tensorflow, usando como
# plataforma o Raspberry Pi
#
# Execucao do software:
# 1 - Setup da aplicacao
# 2 - Configuracao do TensorFlow e aquisicao das imagens
# 3 - Insercao da imagem adquirida em tempo real no algoritimo de detecao
# 4 - Identificacao da acao de comando por imagem
# 5 - Identificacao da acao de comando por distancia
# 6 - Conjuncao booleana (imagem E distancia) para identificacao de acao
# 7 - Execucao da manobra, retorno ao modulo 2
# 8 - Modulos de teste e debugging
#
# Disclaimer: A logica do programa foi elaborada inteiramente pelo gurpo mas
# diversos exemplos foram consultados. O mais influente deles pode ser encontrado em:
# https://github.com/EdjeElectronics/TensorFlow-Object-Detection-on-the-Raspberry-Pi
#
# Importante:
# O script deve rodar diretamente na pasta "object_detection" dentro do Raspberry
# Para buscar por partes inacabadas procure por (crtl+f) "A_DESENVOLVER"

# -----------------------------------------------------------------------------
# SETUP DA APLICACAO
# Neste modulo e feita a:
# importacao das bibliotecas necessarias para a execucao do programa,
# configuracao dos pinos de entrada e saida do Raspberry Pi,
# definicao da compressao da imagem recebida pela camera (HxV pixels)

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
GPIO.setup(M1Controle,GPIO.OUT) #define o pino M1PWM como SAIDA
GPIO.output(M1Frente,GPIO.LOW) #define a SAIDA do pino M1Frente como BAIXA
GPIO.output(M1Tras,GPIO.LOW) #define a SAIDA do pino M1Tras como BAIXA
M1pwm=GPIO.PWM(M1Controle,50) #define o pino M1Controle como saida para um PWM de 50Hz

# Setup dos pinos do MOTOR 2
GPIO.setup(M2Frente,GPIO.OUT) #define o pino M2Frente como SAIDA
GPIO.setup(M2Tras,GPIO.OUT) #define o pino M2Tras como SAIDA
GPIO.setup(M2Controle,GPIO.OUT) #define o pino M2PWM como SAIDA
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

# -----------------------------------------------------------------------------
# EXECUCAO DO SOFTWARE
# Nesta parte do modulo e feita a:
# Selecao da camera: PiCam
# Identificacao do modelo utilizado

#seleciona a camera a ser utilizada
camera_type = 'picamera'

#identifica o modelo
MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'

#pega o PATH do diretorio atual de trabalho
CWD_PATH = os.getcwd()

# PATH do inferece_graph (.pb) que contem o modelo utilizado para deteccao de objetos
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# PATH para o arquivo de label map
PATH_TO_LABELS = os.path.join(CWD_PATH,'data','placas_labelmap.pbtxt')

# Numero de classes detectaveis
NUM_CLASSES = 3

## Carregando o Labelmap
# O indice do labelmap relaciona com um nome de categoria, entao quando a rede
# convolucional preve um '1', sabemos que isso corresponde a placa de 'pare'.

# carrega o labelmap dentro da variavel 'label_map'
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)

# converte os labelmaps em categorias e adiciona a variavel 'categories'
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)

# cria um indice de categorias baseado na variavel 'categories'
category_index = label_map_util.create_category_index(categories)

# carrega o modelo do TensorFlow para a memoria
with tf.Graph().as_default() #wrapper que compatibiliza com TF2.0
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

# Define os Tensores de entrada e saida (dados) para o classificador

# Tensor de entrada e a imagem
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Os tensores de saida sao as caixas de deteccao, scores e classes
# Cada caixa representa uma parte da imagem onde um objeto foi detectado
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# O score representa o nivel de confianca para cada objeto
# O score e apresentado na imagem resultante, junto com um label da classe
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Numero de objetos detectados
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# Inicializa a calculadora de framerate
frame_rate_calc = 1
freq = cv2.getTickFrequency()
font = cv2.FONT_HERSHEY_SIMPLEX

# inicializa variaveis de controle para movimentacao
detected_pare = False
detected_vir_dir = False
detected_vir_esq = False
counter_pare = 0
counter_vir_dir = 0
counter_vir_esq = 0
pause = 0
pause_counter = 0

### FUNCAO DE DETECCAO DE PLACAS E CONTROLE DE MOVIMENTO ###
# essa funcao contem o codigo para detectar 3 placas e determinar o momvimento

def detector_placas(frame):

    # use variaveis globais para que elas retenham o valor apos a execucao da funcao
    global detected_pare, detected_vir_dir, detected_vir_esq
    global pause, pause_counter

    frame_expanded = np.expand_dims(frame, axis=0)

    #executa a deteccao rodando o modelo com a imagem como input
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: frame_expanded})

    #apresenta os resultados da deteccao na tela
    vis_util.visualize_boxes_and_labels_on_image_array(
        frame,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8,
        min_score_thresh=0.40)

    #se a classe detectada for 1, 2 ou 3, incremenda o contador
    if(classes[0][0]==1 and pause==0):
        counter_pare = counter_pare + 1

    elif(classes[0][0]==2 and pause==0):
        counter_vir_esq = counter_vir_esq + 1

    elif(classes[0][0]==3 and pause==0):
        counter_vir_esq = counter_vir_esq + 1

    # se a placa ficar por mais de 10 frames na imagem (6,6 segundos)
    if counter_pare > 10:
        detected_pare = True
        counter_pare = 0
        # Pausa a deteccao ao setar o flag "pause"
        pause = 1

    if counter_vir_esq > 10:
        detected_vir_esq = True
        counter_vir_esq = 0
        # Pausa a deteccao ao setar o flag "pause"
        pause = 1

    if counter_vir_dir > 10:
        detected_vir_dir = True
        counter_vir_dir = 0
        # Pausa a deteccao ao setar o flag "pause"
        pause = 1

    # Incrementa o contador "pause" ate chegar em 5
    # (com um framerate de 1.5 FPS, this e aproximadamente 2 segundos),
    # Entao despausa a aplicacao (set pause = 0).
    if pause == 1:
        pause_counter = pause_counter + 1
        if pause_counter > 3:
            pause = 0
            pause_counter = 0
            detected_pare = False
            detected_vir_dir = False
            detected_vir_esq = False


# A_DESENVOLVER:
# Integracao do TESTE 02 no arquivo Main
# Codigo a escrever:
# executar o controle de movimento utilizando as variaveis "detected_*"
# executar o check de distancia utilizando o HC-SR04

#### Inicializando a camera e executando a deteccao de objetos ####

if camera_type == 'picamera':
    # Inicializa a PiCam e pega a referencia para os dados da captura
    camera = PiCamera()
    camera.resolution = (IM_WIDTH,IM_HEIGHT)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
    rawCapture.truncate(0)

    # Continuamente executa a captura de imagens e aplica a deteccao de objetos nela
    for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):

        t1 = cv2.getTickCount()

        # Adquire o frame e expande as dimensoes para ter o formato: [1, None, None, 3]
        # um vetor de coluna unica, onde cada item na coluna tem o valor RGB do pixel
        frame = frame1.array
        frame.setflags(write=1)

        # passa o frame dentro da funcao de deteccao
        frame = detector_placas(frame)

        # Mostra o FPS
        cv2.putText(frame,"FPS: {0:.2f}".format(frame_rate_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)

        # Mostra todos os resultados.
        cv2.imshow('Object detector', frame)

        # Calculo do FPS
        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc = 1/time1

        # Pressione Q para parar
        if cv2.waitKey(1) == ord('q'):
            break

        rawCapture.truncate(0)

    camera.close()
    GPIO.output(M1Frente,GPIO.LOW) #motor 1 parado
    GPIO.output(M1Tras,GPIO.LOW)
    GPIO.output(M2Frente,GPIO.LOW) #motor 2 parado
    GPIO.output(M2Tras,GPIO.LOW)
    print("Motores desativados")
    M1pwm.ChangeDutyCycle(0) #desativa o dutycycle do motor 1
    M2pwm.ChangeDutyCycle(0) #desativa o dutycycle do motor 2
    print("dutycycle == 0")
    GPIO.cleanup() #limpa o estado de todos os pinos
    print("GPIO cleanup completado")

# -----------------------------------------------------------------------------
# TESTES E DEBUGGING
# Teste 1: ambos os motores para frente ate que alvo esteja a menos de 10cm
# Teste 2: Inicializa o modelo treinado e testa a deteccao com a camera
# Remova o comentario das proximas linhas para chamar este modulo

#testes com o GPIO
import Modulos/Teste_01

#testes de deteccao de modelo
import Modulos/Teste_02
