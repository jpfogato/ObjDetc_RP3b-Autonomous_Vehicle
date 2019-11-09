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


### -------------------------------------------------------------------------------------------
# TESTES: Exemplos de programas para elaboracao de troubleshoots
### -------------------------------------------------------------------------------------------

distancia_min = 35 # centimetros
duty_cycle = 50 # %

# # teste da funcao seguir_em_frente()
# k=0
# while k<2:
#     k = k+1
#     pausa(1)
#     seguir_em_frente(duty_cycle)
# 
# parar_veiculo()
# 
# # teste da funcao virar_a_direita()
# k=0
# while k<2:
#     k = k+1
#     virar_a_direita(duty_cycle)
#     pausa(1)
#     endireitar_rodas()
# 
# parar_veiculo()
# 
# #teste da funcao virar_a_esquerda()
# k=0
# while k<2:
#     k = k+1
#     virar_a_esquerda(duty_cycle)
#     pausa(1)
#     endireitar_rodas()
# 
# parar_veiculo()
# 
# # virar a esquerda por 1 segundo, aguardar 1 segundo, depois virar a direita por 1 segundo
# # repete por k vezes
# k=0
# while k<2:
#     k = k+1
#     virar_a_esquerda(duty_cycle)
#     pausa(1)
#     endireitar_rodas()
#     pausa(1)
#     virar_a_direita(duty_cycle)
#     pausa(1)
#     endireitar_rodas()
#     pausa(1)
# 
# parar_veiculo()
# 
# # teste da funcao identifica_distancia()
# # plota k vezes
# k=0
# fim_do_pulso = 0
# inicio_do_pulso = 0
# while k<5:
#     k = k+1
#     # espera 0,1s antes de executar novamente
#     pausa(0.1)
#     # print da distancia em cm no console
#     print("Distancia medida: ", identifica_distancia(), " cm")
#
# teste da funcao andar ate estar proximo do alvo
# andar_ate_alvo(distancia_min)
#
# parar_veiculo()
#
# teste composto. Elabore rotina como prefirir
# while(1):
#   andar_ate_alvo(distancia_min)
#
#   parar_veiculo()
#
#   pausa(4)
#
#   virar_a_esquerda(80)
#
#   pausa(4)
#
#   finalizar()
#   break
