import RPi.GPIO as GPIO
import time

#trabalha com os pinos fisicos atraves da nomenclatura da GPIO
GPIO.setmode(GPIO.BCM)

# Pinos do sensor HC-SR04 e variaveis utilizadas
TRIGGER = 17 #GPIO 17 - PINO 11 - usado como fonte de TRIGGER
ECHO = 4 #GPIO 04 - PINO 07 - usado como recebedor do pulso
# Setup dos pinos do sensor HC-SR04
GPIO.setup(TRIGGER,GPIO.OUT) #define o pino TRIGGER como SAIDA
GPIO.setup(ECHO,GPIO.IN) #define o pino ECHO como ENTRADA
GPIO.output(TRIGGER,GPIO.LOW) #define a SAIDA do pino TRIGGER como BAIXA
duracao_do_pulso = 0

# Pinos utilizados pelo MOTOR 1
m1Ativo = 25 #GPIO 25 - PINO 22
m1Velocidade = 23 #GPIO 23 - PINO 16
# Setup dos pinos do MOTOR 1
GPIO.setup(m1Ativo,GPIO.OUT) #define o pino m1Ativo como SAIDA
GPIO.setup(m1Velocidade,GPIO.OUT) #define o pino m1pwm como SAIDA
GPIO.output(m1Ativo,GPIO.LOW) #define a SAIDA do pino m1Ativo como BAIXA
m1pwm=GPIO.PWM(m1Velocidade,50) #define o pino m1Velocidade como saida para um PWM de 50Hz
m1pwm.ChangeFrequency(50) # define a frequencia em 50Hz
m1pwm.start(0) #define o dutycycle inicial no motor 1 em 0%

# Pinos utilizados pelo MOTOR: VIRAR
pinoDireita = 20 #GPIO 20 - PINO 38
pinoEsquerda = 16 #GPIO 16 - PINO 36
# Setup dos pinos do MOTOR 2
GPIO.setup(pinoDireita,GPIO.OUT) #define o pino pinoDireita como SAIDA
GPIO.setup(pinoEsquerda,GPIO.OUT) #define o pino pinoEsquerda como SAIDA
GPIO.output(pinoDireita,GPIO.LOW) #define a SAIDA do pino pinoDireita como BAIXA
GPIO.output(pinoEsquerda,GPIO.LOW) #define a SAIDA do pino pinoEsquerda como BAIXA

# FUNCOES:

# Funcao de identificacao de distancia:
# essa funcao dispara um sinal a partir do pino TRIGGER e aguarda uma resposta no pino ECHO
# apos isso, conta o tempo do pulso no pino ECHO e determina a distancia em cm
def indentifica_distancia():
    # essa funcao ativa o pino TRIGGER
    GPIO.output(TRIGGER, True)
    # durante apenas 1us
    time.sleep(0.000001)
    # depois desliga o pino TRIGGER
    GPIO.output(TRIGGER, False)
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

# Funcao seguir em frente
# essa funcao faz o veiculo andar em linha reta
# usar como argumentos: "duty cycle"
def seguir_em_frente(duty_cycle):
    #Desativa os dois pinos do motor que controla a direcao
    GPIO.output(pinoEsquerda, GPIO.LOW)
    GPIO.output(pinoDireita, GPIO.LOW)
    # Ativa o motor 1 com o duty cycle informado
    GPIO.output(m1Ativo, GPIO.HIGH)
    m1pwm.ChangeDutyCycle(duty_cycle)

# Funcao estreitar as rodas
# essa funcao faz as rodas da frente se reorientarem
def endireitar_rodas():
    # Desativa o pinoEsquerda do motor 2
    GPIO.output(pinoEsquerda, GPIO.LOW)
    # Desativa o pinoDireita do motor 2
    GPIO.output(pinoDireita, GPIO.LOW)

# Funcao virar a esquerda
# essa funcao faz o veiculo virar para a esquerda
def virar_a_esquerda():
    # Aciona o pinoEsquerda do motor 2
    GPIO.output(pinoEsquerda, GPIO.HIGH)
    # Desativa o pinoDireita do motor 2
    GPIO.output(pinoDireita, GPIO.LOW)

# Funcao virar a direita
# essa funcao faz o veiculo virar para a esquerda
def virar_a_direita():
    # Aciona o pinoEsquerda do motor 2
    GPIO.output(pinoEsquerda, GPIO.LOW)
    # Desativa o pinoDireita do motor 2
    GPIO.output(pinoDireita, GPIO.HIGH)

# Funcao de movimentacao para frente ate estar em frente a placa
# essa funcao faz o veiculo andar para frente ate que esteja a uma determinada distancia do alvo
# usar como argumentos: "Distancia maxima ate o alvo", "duty cycle"
def andar_para_frente(distancia_max_ate_alvo,duty_cycle):
    # Aciona o motor 1
    GPIO.output(m1Ativo, GPIO.HIGH)
    # define o duty cycle no motor 1
    m1pwm.ChangeDutyCycle(duty_cycle)
    # se a distancia max ate o alvo >= distancia medida pelo sensor de ultrassom
    if distancia_max_ate_alvo >= indentifica_distancia():
        # Desativa o motor 1
        GPIO.output(m1Ativo, GPIO.LOW)

### -------------------------------------------------------------------------------------------
# TESTES:

distancia_max = 20
duty_cycle = 25

# teste da funcao identifica_distancia()
while(1):
    # espera 0,1s antes de executar novamente
    time.sleep(0.1)
    # print da distancia em cm no console
    print("Distancia medida: ", indentifica_distancia(), " cm")

# teste da funcao seguir_em_frente()
while(1):
    seguir_em_frente(duty_cycle)

# teste da funcao virar_a_direita()
while(1):
    virar_a_direita()

#teste da funcao virar_a_esquerda()
while(1):
    virar_a_esquerda()

# teste da funcao andar_para_frente ate estar em frente a placa
while(1):
    andar_para_frente(distancia_max,duty_cycle)

# virar a esquerda por 2 segundos, aguardar 1 segundo, depois virar a direita por 2 segundos
while(1):
    virar_a_esquerda()
    time.sleep(2)
    endireitar_rodas()
    time.sleep(1)
    virar_a_direita()
    time.sleep(2)
    endireitar_rodas()
    time.sleep(1)
