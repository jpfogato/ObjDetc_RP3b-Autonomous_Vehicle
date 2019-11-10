import RPi.GPIO as GPIO

# trabalha com os pinos fisicos atraves da nomenclatura da GPIO
GPIO.setmode(GPIO.BCM)

#desativa todos os alarmes dos pinos
GPIO.setwarnings(False)

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

cleanup()
