import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) #trabalha com os pinos fisicos atraves da nomenclatura da GPIO

# Pinos do sensor HC-SR04
TRIGGER = 17 #GPIO 17 - PINO 11 - usado como fonte de TRIGGER
ECHO = 4 #GPIO 04 - PINO 07 - usado como recebedor do pulso
# Setup dos pinos do sensor HC-SR04
GPIO.setup(TRIGGER,GPIO.OUT) #define o pino TRIGGER como SAIDA
GPIO.setup(ECHO,GPIO.IN) #define o pino ECHO como ENTRADA
GPIO.output(TRIGGER,GPIO.LOW) #define a SAIDA do pino TRIGGER como BAIXA

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

# Modulo de testes para validar integracao entre motores e sensor de ultrasom

print("Modulo de Debug e Teste 8")
print("teste 1: ambos motores para frente ate que alvo esteja a menos de 10cm")
print("Para iniciar digite 's' ")
print("para abortar o teste digite 'n'")

distancia=10000

while(1):

    entrada=input() #espera a entrada do usuario

    while entrada=='s': #caso o usuario digite S o progra e iniciado
        GPIO.output(m1Ativo,GPIO.HIGH) #motor 1 para frente
        m1pwm.ChangeDutyCycle(25) #define o dutycycle no motor 1 em 25%
        while distancia>=10: #enquanto a distancia for maior ou igual a 10
            GPIO.output(TRIGGER,GPIO.HIGH) #define o valor de TRIGGER como ALTO...
            time.sleep(0.000001) #...durante apenas 1us para que o sensor envie um pulso de 40kHz
            GPIO.output(TRIGGER,GPIO.LOW) #finaliza o pulso
            while GPIO.input(ECHO)==0:
                pulse_start=time.time() #inicia uma contagem que se encerra na borda de SUBIDA do pino ECHO
            while GPIO.input(ECHO)==1:
                pulse_end=time.time() #inicia uma contagem que se encerra na borda de DESCIDA do pino ECHO
            duracao_pulso = pulse_end - pulse_start #conta o tempo em segundos para a duracao do pulso
            distancia = round((duracao_pulso * 17000),2) #calcula a distancia em cm e arredonda em 2 casas
            print("Distancia medida: ", distancia," cm") #informa a distancia pode ser comentado
        GPIO.output(m1Ativo,GPIO.LOW) #motor 1 parado
        #GPIO.output(pinoDireita,GPIO.LOW) #motor 2 parado
        #GPIO.output(pinoEsquerda,GPIO.LOW)
        m1pwm.ChangeDutyCycle(0) #desativa o dutycycle do motor 1
        print("Motores desativados")

    elif entrada=='n': #caso o usuario digite N o programa e interrompido
        GPIO.output(m1Ativo,GPIO.LOW) #motor 1 parado
        GPIO.output(pinoDireita,GPIO.LOW) #motor 2 parado
        GPIO.output(pinoEsquerda,GPIO.LOW)
        print("Motores desativados")
        m1pwm.ChangeDutyCycle(0) #desativa o dutycycle do motor 1
        M2pwm.ChangeDutyCycle(0) #desativa o dutycycle do motor 2
        print("dutycycle == 0")
        GPIO.cleanup() #limpa o estado de todos os pinos
        print("GPIO cleanup completado")
        break

    else:
        print("Digite a letra correta")
        print("Para iniciar digite 's' ")
        print("Para abortar o teste digite 'n'")
