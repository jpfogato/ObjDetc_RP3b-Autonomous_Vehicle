import time

# Funcao de identificacao de distancia:
# essa funcao dispara um sinal a partir do pino TRIGGER e aguarda uma resposta no pino ECHO
# apos isso, conta o tempo do pulso no pino ECHO e determina a distancia em cm
def indentifica_distancia(echo):
    # essa funcao ativa o pino TRIGGER
    print("TRIGGER = HIGH")
    # durante apenas 1us
    time.sleep(0.000001)
    # depois desliga o pino TRIGGER
    print("TRIGGER = LOW")
    # e define que enquanto ECHO possuir um valor logico BAIXO
    while echo == 0:
        # pega uma referencia de tempo para usar como timestamp
        inicio_do_pulso = time.time()
        echo = 1
        # assim que o valor logico de ECHO muda para ALTO
    while echo == 1:
        # o software conta o tempo enquanto esse pulso se manter em nivel logico ALTO
        time.sleep(15/17000)
        fim_do_pulso = time.time()
        echo = 0
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
    print("m1Ativo = LOW")
    print("Duty Cycle = 0")

# Funcao seguir em frente
# essa funcao faz o veiculo andar em linha reta
# usar como argumentos: "duty cycle"
def seguir_em_frente(duty_cycle):
    print("pinoEsquerda = LOW")
    print("pinoDireita = LOW")
    # Ativa o motor 1 com o duty cycle informado
    print("m1Ativo = HIGH")
    print("Duty Cycle: ", duty_cycle)
    print("----------------------------------")

# Funcao endireitar as rodas
# essa funcao faz as rodas da frente se reorientarem
def endireitar_rodas():
    # Desativa o pinoEsquerda do motor 2
    print("pinoEsquerda = LOW")
    # Desativa o pinoDireita do motor 2
    print("pinoDireita = LOW")
    print("----------------------------------")

# Funcao virar a esquerda
# essa funcao faz o veiculo virar para a esquerda
def virar_a_esquerda():
    # Aciona o pinoEsquerda do motor 2
    print("pinoEsquerda = HIGH")
    # Desativa o pinoDireita do motor 2
    print("pinoDireita = LOW")
    print("----------------------------------")

# Funcao virar a direita
# essa funcao faz o veiculo virar para a esquerda
def virar_a_direita():
    # Desativa o pinoEsquerda do motor 2
    print("pinoEsquerda = LOW")
    # Aciona o pinoDireita do motor 2
    print("pinoDireita = HIGH")
    print("----------------------------------")

# Funcao de movimentacao para frente ate estar em frente a placa
# essa funcao faz o veiculo andar para frente ate que esteja a uma determinada distancia do alvo
# usar como argumentos: "Distancia maxima ate o alvo", "duty cycle"
def andar_ate_alvo(distancia_max_ate_alvo,duty_cycle):
    # Aciona o motor 1
    print("m1Ativo = HIGH")
    # define o duty cycle no motor 1
    print("Duty Cycle: " , duty_cycle,)
    # se a distancia max ate o alvo >= distancia medida pelo sensor de ultrassom
    if distancia_max_ate_alvo >= indentifica_distancia(0):
        # Desativa o motor 1
        print("m1Ativo = LOW")
        return True
    print("----------------------------------")

def cleanup():
    print("m1Ativo = LOW")  # motor 1 parado
    print("pinoDireita = LOW")  # motor 2 parado
    print("pinoEsquerda = LOW")
    print("Duty Cycle = 0")
    print("GPIO.cleanup()")  # limpa o estado de todos os pinos
    print("GPIO cleanup completado")

# -------------------------------------------------------------------------------------------
# TESTES:

distancia_max = 20
duty_cycle = 25

# teste da funcao seguir_em_frente()
k=0
while(k<5):
    k = k+1
    time.sleep(1)
    seguir_em_frente(duty_cycle)

parar_veiculo()

# teste da funcao virar_a_direita()
k=0
while(k<5):
    k = k+1
    time.sleep(1)
    virar_a_direita()

#teste da funcao virar_a_esquerda()
k=0
while(k<5):
    k = k+1
    time.sleep(1)
    virar_a_esquerda()


# virar a esquerda por 1 segundo, aguardar 1 segundo, depois virar a direita por 1 segundo
# repete por k vezes
k=0
while(k<5):
    k = k+1
    virar_a_esquerda()
    time.sleep(1)
    endireitar_rodas()
    time.sleep(1)
    virar_a_direita()
    time.sleep(1)
    endireitar_rodas()
    time.sleep(1)


#teste da funcao identifica_distancia()
k=0
while(k<20):
    k = k+1
    # espera 0,1s antes de executar novamente
    time.sleep(0.1)
    # print da distancia em cm no console
    print("Distancia medida: ", indentifica_distancia(0), " cm")

# teste da funcao andar_para_frente ate estar em frente a placa
while(andar_ate_alvo(100,duty_cycle)==False):
    print(indentifica_distancia(0))
    andar_ate_alvo(distancia_max,duty_cycle)
    print("----------------------------------")

parar_veiculo()

cleanup()