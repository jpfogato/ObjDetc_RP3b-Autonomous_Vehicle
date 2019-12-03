import RPi.GPIO as GPIO
import time
import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import tensorflow as tf

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
GPIO.output(esquerda, GPIO.LOW)  # define a SAIDA do pino esquerda como B


### -------------------------------------------------------------------------------------------
# FUNCOES:
### -------------------------------------------------------------------------------------------

# Esta funcao faz uma pausa na execucao do codigo
# Argumento: Tempo [s]
def pausa(tempo):
    time.sleep(tempo)

# Funcao de identificacao de distancia:
# essa funcao dispara um sinal a partir do pino TRIGGER e aguarda uma resposta no pino ECHO
# apos isso, conta o tempo do pulso no pino ECHO e determina a distancia em cm
def identifica_distancia():
    global inicio_do_pulso
    global fim_do_pulso
    global duracao_do_pulso
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

# esta funcao reseta os contadores
def resetar_contadores():
    count_pare = 0
    count_vir_esq = 0
    count_vir_dir = 0

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

# Inicializa a camera e inicia a deteccao de objetos

if camera_type == 'picamera':
    # Inicializa a PiCam e pega a referencia para os dados da captura
    camera = PiCamera()
    camera.resolution = (IM_WIDTH,IM_HEIGHT)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
    rawCapture.truncate(0)

pause = 0
count_vir_dir = 0
count_vir_esq = 0
count_pare = 0
placa_vir_dir = False
placa_vir_esq = False
placa_pare = False
distancia_minima = 40
duty_cycle = 60
tempo_de_pausa = 4

for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):

        t1 = cv2.getTickCount()

        # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        frame = np.copy(frame1.array)
        frame.setflags(write=1)
        frame_expanded = np.expand_dims(frame, axis=0)

        # Perform the actual detection by running the model with the image as input
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: frame_expanded})

        if double(classes[0][0]) == 1 and scores[0][0] >= 0.3:
            count_vir_dir = count_vir_dir +1
        elif double(classes[0][0]) == 2 and scores[0][0] >= 0.6:
            count_vir_esq = count_vir_esq +1
        elif double(classes[0][0]) == 3 and scores[0][0] >= 0.5:
            count_pare = count_pare +1
        else:
            print("nenhuma placa detectada")

        if count_vir_dir >= 10: #placa vir dir detectada por 10 ou mais frames
            placa_vir_dir = True
            resetar_contadores()
        elif count_vir_esq >= 10: #placa vir_esq detectada por 10 ou mais frames
            placa_vir_esq = True
            resetar_contadores()
        elif count_pare >=10: #placa pare detectada por 10 frames ou mais
            placa_pare = True
            resetar_contadores()
        else:
            placa_vir_dir = False
            placa_vir_esq = False
            placa_pare = False

        while True:
            if placa_vir_dir == True and identifica_distancia() <= distancia_minima:
                virar_a_direita(duty_cycle)
                pausa(tempo_de_pausa)
                endireitar_rodas()
            elif placa_vir_esq == True and identifica_distancia() <= distancia_minima:
                virar_a_esquerda(duty_cycle)
                pausa(tempo_de_pausa)
                endireitar_rodas()
            elif placa_pare == True and identifica_distancia() <= distancia_minima:
                 parar_veiculo()
                 endireitar_rodas()
                 pausa(tempo_de_pausa)
            else:
                andar_ate_alvo(distancia_minima)
            break

        rawCapture.truncate(0)
        
        camera.close()
