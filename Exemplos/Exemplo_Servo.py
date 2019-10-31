# sudo python ARQUIVO.py -> usar no raspberry para iniciar o script pelo Shell
# nano ARQUIVO.py -> abre o arquivo *.py no shell do Raspberry

#caso a quantidade de pinos PWM seja insuficiente, testar http://abyz.me.uk/rpi/pigpio/python.html
#instalar no Pi: sudo pigpiod
#pi=pigpio.pi()
#import pigpio



import RPi.GPIO as GPIO #importa a biblioteca GPIO para o Rasbperry Pi
GPIO.setmode(GPIO.BOARD) #define a numeracao dos pinos como os pinos fisicos no hardware

GPIO.cleanup() # retorna os pinos para o estado natural

servo=11 #define o pino conectado ao servomotor

pwm_servo=GPIO.PWM(servo,50) #define a frequencia do sinal de controle como 50Hz

pwm_servo.start(0) # define o Duty Cycle como 0

# ANTES DE RODAR O SCRIPT, TESTAR COM O MOTOR:
# Qual o Duty Cycle para 0º (virar a direita)? ---->
# Qual o Duty Cycle para 90º (seguir em frente)? -->
# Qual o Duty Cycle para 180º (virar a esquerda)? ->

while(1)
    duty_cycle=input("Insira O Duty Cycle: ") #
    pwm_servo.ChangeDutyCycle(duty_cycle)

pwm_servo.stop()
GPIO.cleanup() # retorna os pinos para o estado natural
