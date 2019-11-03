# Modulo de testes para validar integracao entre motores e sensor de ultrasom

print("Modulo de Debug e Teste 8")
print("teste 1: ambos motores para frente ate que alvo esteja a menos de 10cm")
print("Para iniciar digite 's' ")
print("para abortar o teste digite 'n'")

while(1):

    entrada=input() #espera a entrada do usuario

    if entrada=='s': #caso o usuario digite S o progra e iniciado
        GPIO.output(M1Frente.HIGH) #motor 1 para frente
        GPIO.output(M1Tras.LOW)
        GPIO.output(M2Frente.HIGH) #motor 2 para frente
        GPIO.output(M2Tras.LOW)
        M1pwm.ChangeDutyCycle(50) #define o dutycycle no motor 1 em 50%
        M2pwm.ChangeDutyCycle(50) #define o dutycycle no motor 2 em 50%
        while distancia>=10: #enquanto a distancia for maior ou igual a 10
            GPIO.output(TRIGGER.HIGH) #define o valor de TRIGGER como ALTO...
            time.sleep(0.000001) #...durante apenas 1us para que o sensor envie um pulso de 40kHz
            GPIO.output(TRIGGER.LOW) #finaliza o pulso
            while GPIO.input(ECHO)==0:
                pulse_start=time.time() #inicia uma contagem que se encerra na borda de SUBIDA do pino ECHO
            while GPIO.input(ECHO)==1:
                pulse_end=time.time() #inicia uma contagem que se encerra na borda de DESCIDA do pino ECHO
            duracao_pulso = pulse_end - pulse_start #conta o tempo em segundos para a duracao do pulso
            distancia = round((duracao_pulso * 17000),2) #calcula a distancia em cm e arredonda em 2 casas
            print("Distancia medida: ", distancia," cm") #informa a distancia pode ser comentado
        GPIO.output(M1Frente,GPIO.LOW) #motor 1 parado
        GPIO.output(M1Tras,GPIO.LOW)
        GPIO.output(M2Frente,GPIO.LOW) #motor 2 parado
        GPIO.output(M2Tras,GPIO.LOW)
        M1pwm.ChangeDutyCycle(0) #desativa o dutycycle do motor 1
        M2pwm.ChangeDutyCycle(0) #desativa o dutycycle do motor 2
        print("Motores desativados")

    elif entrada=='n': #caso o usuario digite N o programa e interrompido
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
        break

    else:
        print("Digite a letra correta")
        print("Para iniciar digite 's' ")
        print("Para abortar o teste digite 'n'")
