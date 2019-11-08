# sudo python ARQUIVO.py -> usar no raspberry para iniciar o script pelo Shell
# nano ARQUIVO.py -> abre o arquivo *.py no shell do Raspberry

import RPi.GPIO as GPIO #importa a biblioteca GPIO para o Rasbperry Pi
GPIO.setmode(GPIO.BOARD) #define a numeracao dos pinos como os pinos fisicos no hardware

GPIO.cleanup() # retorna os pinos para o estado natural

motor_esq=11 # define o motor esquerdo como pino 11
GPIO.setup(motor_esq,GPIO.OUT) # define o pino do motor esquerdo como uma saida

motor_dir=13 #define o motor direito como pino 13
GPIO.setup(motor_dir,GPIO.OUT) # define o pino do motor direito como uma saida


# criando um objeto pwm_esq e pwm_dir (PWM direito e esquerdo)
pwm_esq = GPIO.PWM(motor_esq,50) # (pino,frequencia) - 50Hz = 20ms
pwm_dir = GPIO.PWM(motor_dir,50) # (pino,frequencia) - 50Hz = 20ms

# inicia o objeto PWM
pwm_esq.start(0) # define o duty cycle em 0% - 0% desligado, 100% ligado completamente
pwm_dir.start(0) # define o duty cycle em 0% - 0% desligado, 100% ligado completamente

# controle de Duty Cycle feito pelo usuário:

while(1):
        duty_cycle_esq=input("Duty Cycle para o  motor esquerdo (0-100): ")
        pwm_esq.ChangeDutyCycle(duty_cycle_esq)

        duty_cycle_dir=input("Duty Cycle para o  motor direito (0-100): ")
        pwm_esq.ChangeDutyCycle(duty_cycle_dir)

pwm_esq.stop()
pwm_dir.stop()
GPIO.cleanup() # retorna os pinos para o estado natural

# -----------------------
## TROUBLESHOOT:
# colocar um pino como True
# GPIO.output(pino,True)

# definir valor BAIXO para um pino
# GPIO.output(pino,False)
# -----------------------

# -----------------------
# OUTRAS FUNcoES uTEIS:
#pwm_e/d.ChangeDutyCycle(10) # muda o PWM para o duty cycle selecionado
#pwm_e/d.ChangeFrequency(50) # muda a frequencia do PWM (até 1k?)
# -----------------------
