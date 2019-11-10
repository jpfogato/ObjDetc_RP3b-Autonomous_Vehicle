# software disponivel em github.com/jpfogato
#
# Este software controla um veiculo autonomo controlado por visao de maquina, com auxilio de rede neural
# implementada no tensorflow, usando como plataforma o Raspberry Pi
#
# Importante:
# O script deve rodar diretamente na pasta "object_detection" dentro do Raspberry
#
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
import sys
import RPi.GPIO as GPIO
import time

# trabalha com os pinos fisicos atraves da nomenclatura da GPIO
GPIO.setmode(GPIO.BCM)

# Pinos do sensor HC-SR04
TRIGGER = 17  # GPIO 17 - PINO 11 - usado como fonte de TRIGGER
ECHO = 4  # GPIO 04 - PINO 07 - usado como recebedor do pulso
# Setup dos pinos do sensor HC-SR04
GPIO.setup(TRIGGER, GPIO.OUT)  # define o pino TRIGGER como SAIDA
GPIO.setup(ECHO, GPIO.IN)  # define o pino ECHO como ENTRADA
GPIO.output(TRIGGER, GPIO.LOW)  # define a SAIDA do pino TRIGGER como BAIXA

# Pinos utilizados pelo MOTOR de Propulsao
frente = 25  # GPIO 25 - PINO 22
velocidade = 23  # GPIO 23 - PINO 16
# Setup dos pinos do MOTOR 1
GPIO.setup(frente, GPIO.OUT)  # define o pino frente como SAIDA
GPIO.setup(velocidade, GPIO.OUT)  # define o pino pwm como SAIDA
GPIO.output(frente, GPIO.LOW)  # define a SAIDA do pino frente como BAIXA
pwm = GPIO.PWM(velocidade, 50)  # define o pino velocidade como saida para um PWM de 50Hz
pwm.ChangeFrequency(50)  # define a frequencia em 50Hz
pwm.start(0)  # define o dutycycle inicial no motor 1 em 0%

# Pinos utilizados pelo motor de propulsao
direita = 16  # GPIO 16 - PINO 36
esquerda = 20  # GPIO 20 - PINO 38
# Setup dos pinos do motor de virar
GPIO.setup(direita, GPIO.OUT)  # define o pino direita como SAIDA
GPIO.setup(esquerda, GPIO.OUT)  # define o pino esquerda como SAIDA
GPIO.output(direita, GPIO.LOW)  # define a SAIDA do pino direita como BAIXA
GPIO.output(esquerda, GPIO.LOW)  # define a SAIDA do pino esquerda como BAIXA


# setup de constantes da camera
IM_WIDTH = 800 #800 pixels horizontais
IM_HEIGHT = 600 #600 pixels verticais

# adiciona os comandos ao ambiente PATH do Linux
sys.path.append('..')

# Importa utils do algoritimo de deteccao
from utils import label_map_util #funcoes de verificacao de labels
from utils import visualization_utils as vis_util #funcoes de vizualizacao


### ----------------------------------------------------------------------
### FUNÇÕES
### ----------------------------------------------------------------------

# Esta funcao faz uma pausa na execucao do codigo
# Argumento: Tempo [s]
def pausa(tempo):
    time.sleep(tempo)

# Funcao de identificacao de distancia:
# essa funcao dispara um sinal a partir do pino TRIGGER e aguarda uma resposta no pino ECHO
# apos isso, conta o tempo do pulso no pino ECHO e determina a distancia em cm
def identifica_distancia():
    # essa funcao ativa o pino TRIGGER
    GPIO.output(TRIGGER, GPIO.HIGH)
    # durante apenas 1us
    time.sleep(0.000001)
    # depois desliga o pino TRIGGER
    GPIO.output(TRIGGER, GPIO.LOW)
    # e define que enquanto ECHO possuir um valor logico BAIXO
    while GPIO.input(ECHO) == 0:
        # conta o tempo para usar como timestamp
        inicio_do_pulso = time.time()
        # assim que o valor logico de ECHO muda para ALTO
    while GPIO.input(ECHO) == 1:
        # o software conta o tempo enquanto esse pulso se manter em nivel logico ALTO
        fim_do_pulso = time.time()
    # apos isso, o software faz a contagem do fim do pulso MENOS o inicio do pulso e determina a duracao
    duracao_do_pulso = fim_do_pulso - inicio_do_pulso
    # para entao calcular a distancia em cm
    distancia = duracao_do_pulso * 17000
    # arredonda o valor em 2 casas decimais por conveniencia
    distancia = round(distancia, 2)
    # e devolve o valor para o uso subsequente
    return distancia

# Funcaoo desativar motor de propulsao
# essa funcao faz o veiculo parar imediatamente
def parar_veiculo():
    GPIO.output(frente, GPIO.LOW)
    pwm.ChangeDutyCycle(0)

# Funcao endireitar as rodas
# essa funcao faz as rodas da frente se reorientarem
def endireitar_rodas():
    # Desativa o pino esquerda do motor de virar
    GPIO.output(esquerda, GPIO.LOW)
    # Desativa o pino direita do motor de virar
    GPIO.output(direita, GPIO.LOW)

# Funcao seguir em frente
# esta funcao faz o veiculo andar em linha reta
# usar como argumentos: "duty cycle"
def seguir_em_frente(dutycycle):
    endireitar_rodas()
    # Ativa o motor 1 com o duty cycle informado
    GPIO.output(frente, GPIO.HIGH)
    pwm.ChangeDutyCycle(dutycycle)

# Funcao virar a esquerda
def virar_a_esquerda(dutycycle):
    GPIO.output(esquerda, GPIO.HIGH)
    GPIO.output(direita, GPIO.LOW)
    # Ativa o motor 1 com o duty cycle informado
    GPIO.output(frente, GPIO.HIGH)
    pwm.ChangeDutyCycle(dutycycle)

# Funcao virar a direita
def virar_a_direita(duty_cycle):
    GPIO.output(esquerda, GPIO.LOW)
    GPIO.output(direita, GPIO.HIGH)
    # Ativa o motor 1 com o duty cycle informado
    GPIO.output(frente, GPIO.HIGH)
    pwm.ChangeDutyCycle(duty_cycle)

# Esta funcao faz o veiculo andar para frente ate que esteja a uma determinada distancia do alvo
# Argumentos: "Distancia maxima ate o alvo", "duty cycle"
def andar_ate_alvo(distancia_minima):
    seguir_em_frente(duty_cycle)
    # se a distancia max ate o alvo >= distancia medida pelo sensor de ultrassom
    while distancia_minima < identifica_distancia():
        seguir_em_frente(duty_cycle)
    # Desativa o motor de propulsao
    parar_veiculo()

# esta funcao executa a reconfiguracao dos IOs para um estado seguro
def cleanup():
    # Parar motor de propulsao
    GPIO.output(frente, GPIO.LOW)
    # Parar motor de direcao
    GPIO.output(direita, GPIO.LOW)
    GPIO.output(esquerda, GPIO.LOW)
    pwm.ChangeDutyCycle(0)  # desativa o dutycycle do motor de propulsao
    GPIO.cleanup()  # limpa o estado de todos os pinos
    print("GPIO cleanup completado")

# esta funcao encerra a operacao do veiculo
def finalizar():
    endireitar_rodas()
    parar_veiculo()
    cleanup()
    camera.close()

### ----------------------------------------------------------------------
### EXECUÇÃO
### ----------------------------------------------------------------------

#seleciona a camera a ser utilizada
camera_type = 'picamera'
#identifica o modelo
MODEL_NAME = 'placas_model'
#pega o PATH do diretorio atual de trabalho
CWD_PATH = os.getcwd()
# PATH do inferece_graph (.pb) que contem o modelo utilizado para deteccao de objetos
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
# PATH para o arquivo de label map
PATH_TO_LABELS = os.path.join(CWD_PATH,'data','placas_labelmap.pbtxt')
# Numero de classes detectaveis
NUM_CLASSES = 3
## Carregando o Labelmap
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
# converte os labelmaps em categorias e adiciona a variavel 'categories'
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
# cria um indice de categorias baseado na variavel 'categories': '1' = PARE | '2' = VIR_DIR | '3' = VIR_ESQ.
category_index = label_map_util.create_category_index(categories)

# carrega o modelo do TensorFlow para a memoria
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

# inicializa variaveis de controle para movimentacao
detected_pare = False
detected_vir_dir = False
detected_vir_esq = False
pause = 0
pause_counter = 0


# essa funcao contem o codigo para detectar 3 placas e determinar o momvimento
def detector_placas(frame, pause):
    # use variaveis globais para que elas retenham o valor apos a execucao da funcao
    global detected_pare, detected_vir_dir, detected_vir_esq
    global pause, pause_counter
    frame_expanded = np.expand_dims(frame, axis=0)
    #executa a deteccao rodando o modelo com a imagem como input
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: frame_expanded})
    # #apresenta os resultados da deteccao na tela
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
    if classes[0][0]==1 and pause==0:
        counter_pare = counter_pare + 1
    elif classes[0][0]==2 and pause==0:
        counter_vir_esq = counter_vir_esq + 1
    elif classes[0][0]==3 and pause==0:
        counter_vir_dir = counter_vir_dir + 1
    # se a placa ficar por mais de 10 frames na imagem
    if counter_pare > 10:
        detected_pare = True
        print("detected_pare")
        counter_pare = 0
        # Pausa a deteccao ao setar o flag "pause"
        pause = 1
    if counter_vir_esq > 10:
        detected_vir_esq = True
        print("detected_vir_esq")
        counter_vir_esq = 0
        # Pausa a deteccao ao setar o flag "pause"
        pause = 1
    if counter_vir_dir > 10:
        detected_vir_dir = True
        print("detected_vir_dir")
        counter_vir_dir = 0
        # Pausa a deteccao ao setar o flag "pause"
        pause = 1
    # Incrementa o contador "pause" ate chegar em 5
    # (com um framerate de 1.5 FPS, this e aproximadamente 2 segundos),
    # Entao despausa a aplicacao (set pause = 0).
    if pause == 1:
        pause_counter = pause_counter + 1
        if pause_counter > 5:
            pause = 0
            pause_counter = 0
            detected_pare = False
            detected_vir_dir = False
            detected_vir_esq = False
    return frame

if camera_type == 'picamera':
    # Inicializa a PiCam e pega a referencia para os dados da captura
    camera = PiCamera()
    camera.resolution = (IM_WIDTH,IM_HEIGHT)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
    rawCapture.truncate(0)
    # Continuamente executa a captura de imagens e aplica a deteccao de objetos nela
    for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
        # t1 = cv2.getTickCount()
        # Adquire o frame e expande as dimensoes para ter o formato: [1, None, None, 3]
        # um vetor de coluna unica, onde cada item na coluna tem o valor RGB do pixel
        frame = frame1.array
        frame.setflags(write=1)
        # passa o frame dentro da funcao de deteccao
        frame = detector_placas(frame, 0)
        # Mostra o FPS
        #cv2.putText(frame,"FPS: {0:.2f}".format(frame_rate_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)
        # Mostra todos os resultados.
        #cv2.imshow('Object detector', frame)
        # Calculo do FPS
        #t2 = cv2.getTickCount()
        #time1 = (t2-t1)/freq
        #frame_rate_calc = 1/time1
        # Pressione Q para parar
        if cv2.waitKey(1) == ord('q'):
            break
        rawCapture.truncate(0)

    finalizar()