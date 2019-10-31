# sudo python ARQUIVO.py -> usar no raspberry para iniciar o script pelo Shell
# nano ARQUIVO.py -> abre o arquivo *.py no shell do Raspberry

# ANTES DE CONECTAR O SENSOR, SEGUIR AS CONEXOES CONFORME DESCRITO EM:
# https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

import RPi.GPIO as GPIO #importa a biblioteca GPIO para o Rasbperry Pi
import time #importa bibliotecas de temporizacao
GPIO.setmode(GPIO.BCM) #trabalha com os pinos fisicos atraves da nomenclatura da GPIO

#GPIO.cleanup() # retorna os pinos para o estado natural

# Pinos do sensor HC-SR04
TRIGGER = 17 #GPIO 17 - PINO 11 - usado como fonte de TRIGGER
ECHO = 4 #GPIO 04 - PINO 07 - usado como recebedor do pulso

GPIO.setup(TRIGGER,GPIO.OUT) #define o pino TRIGGER como saida
GPIO.setup(ECHO,GPIO.IN) #define o pino ECHO como Entrada

GPIO.output(TRIGGER, False) #garante que a saida do TRIGGER e baixa

time.sleep(1) #espera 1 segundos para garantir o envio do comando

GPIO.output(TRIGGER,True) #define o valor de TRIGGER como ALTO...
time.sleep(0.000001) #...durante apenas 1us para que o sensor envie um pulso de 40kHz
GPIO.output(ECHO,False) #finaliza o pulso

while GPIO.input(ECHO)==0:
    pulse_start=time.time() #inicia uma contagem que se encerra na borda de SUBIDA do pino ECHO

while GPIO.input(ECHO)==1:
    pulse_end=time.time() #inicia uma contagem que se encerra na borda de DESCIDA do pino ECHO

duracao_pulso = pulse_end - pulse_start

distancia = pulse_duration * 17150 #calculo da distancia baseado no pulso emitido

distancia = round(distancia,2) #numero com apenas 2 casas decimais

print("distancia:", distancia, " cm")

GPIO.cleanup()
