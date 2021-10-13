import sim
import numpy as np
import time
import simConst
import garra
import motor
import sensor
import girar
import visionAlgo

## FUNÇÕES DO CUBO ######################################

def alinhar_e_pegar_cubo(object, bloco_escolhido):
    '''
    status_garra indica se é para usar a garra da frente ou das costas
    posicao_cubo indica se o cubo a ser pego está na esquerda ou na direita do quadrado da arena
    bloco_escolhido vem no formato ['Tipo do bloco', area do bloco, sub area do bloco]
    'Tipo do bloco' é um caractere, onde W = branco(numeros), K = preto(codigo de barras), 0 = vazio, o resto é colorido
    '''
    
    #Escolhe para qual lado do quadrado o robo tem que ir para se alinhar com o cubo
    if bloco_escolhido[1] == 0:
        if bloco_escolhido[2] == 0:
            posicao_cubo = 'direita'
        elif bloco_escolhido[2] == 1:
            posicao_cubo = 'esquerda'
        elif bloco_escolhido[2] == 2:
            posicao_cubo = 'direita'
        elif bloco_escolhido[2] == 3: #bloco escondido
            posicao_cubo = 'esquerda'
        
    elif bloco_escolhido[1] == 1:
        if bloco_escolhido[2] == 0:
            posicao_cubo = 'direita'
        elif bloco_escolhido[2] == 1:
            posicao_cubo = 'esquerda'
        elif bloco_escolhido[2] == 2: #bloco escondido
            posicao_cubo = 'direita'
        elif bloco_escolhido[2] == 3:
            posicao_cubo = 'esquerda'

    elif bloco_escolhido[1] == 4: #era 2, mudei para 4
        if bloco_escolhido[2] == 0:
            posicao_cubo = 'direita'
        elif bloco_escolhido[2] == 1:
            posicao_cubo = 'esquerda'
        elif bloco_escolhido[2] == 2:
            posicao_cubo = 'direita'
        elif bloco_escolhido[2] == 3: #bloco escondido
            posicao_cubo = 'esquerda'

    elif bloco_escolhido[1] == 5: #era 3, mudei para 5
        if bloco_escolhido[2] == 0:
            posicao_cubo = 'direita'
        elif bloco_escolhido[2] == 1:
            posicao_cubo = 'esquerda'
        elif bloco_escolhido[2] == 2: #bloco escondido
            posicao_cubo = 'direita'
        elif bloco_escolhido[2] == 3:
            posicao_cubo = 'esquerda'

    elif bloco_escolhido[1] == 2: #era 4, mudei para 2
        if bloco_escolhido[2] == 0:
            posicao_cubo = 'esquerda'
        elif bloco_escolhido[2] == 1: #bloco escondido
            posicao_cubo = 'direita'
        elif bloco_escolhido[2] == 2:
            posicao_cubo = 'esquerda'
        elif bloco_escolhido[2] == 3:
            posicao_cubo = 'direita'

    elif bloco_escolhido[1] == 3: #era 5, mudei para 3
        if bloco_escolhido[2] == 0: #bloco escondido
            posicao_cubo = 'esquerda'
        elif bloco_escolhido[2] == 1:
            posicao_cubo = 'direita'
        elif bloco_escolhido[2] == 2:
            posicao_cubo = 'esquerda'
        elif bloco_escolhido[2] == 3:
            posicao_cubo = 'direita'

    elif bloco_escolhido[1] == 6:
        if bloco_escolhido[2] == 0:
            posicao_cubo = 'esquerda'
        elif bloco_escolhido[2] == 1: #bloco escondido
            posicao_cubo = 'direita'
        elif bloco_escolhido[2] == 2:
            posicao_cubo = 'esquerda'
        elif bloco_escolhido[2] == 3:
            posicao_cubo = 'direita'
            
    elif bloco_escolhido[1] == 7:
        if bloco_escolhido[2] == 0: #bloco escondido
            posicao_cubo = 'esquerda'
        elif bloco_escolhido[2] == 1:
            posicao_cubo = 'direita'
        elif bloco_escolhido[2] == 2:
            posicao_cubo = 'esquerda'
        elif bloco_escolhido[2] == 3:
            posicao_cubo = 'direita'

    #Se alinha com o cubo
    if posicao_cubo == 'direita' or posicao_cubo == 'esquerda': #acho que pode tirar esse IF
        motor.alinharLateral(object, posicao_cubo) #alinha com o lado do quadrado onde está o cubo a ser pego

    #Alinhar com a partes de trás do quadrado, para que a garra não bata no cubo quando descer
    motor.andar_em_metros(object, 'frente', 2, 0.01)
    motor.alinhar(object, 'tras')
    motor.andar_em_metros(object, 'frente', 1, 0.030) #andar para frente para identificar melhor o cubo
    if posicao_cubo == 'direita':
        motor.andar_em_metros(object, 'esquerda', 1, 0.015)
    if posicao_cubo == 'esquerda':
        motor.andar_em_metros(object, 'esquerda', 1, 0.02)

    

    #Ve o valor númerico(ou cor) do bloco a ser pego
    if bloco_escolhido[0] == 'W': #bloco branco de numeros
        numero_bloco = visionAlgo.getNumber(object)
        if numero_bloco[0] == 'empty':
            motor.andar_em_metros(object,'direita',1,0.02)
            numero_bloco = visionAlgo.getNumber(object)
        numero_bloco = numero_bloco[0]
    elif bloco_escolhido[0] == 'K': #bloco preto de codigo de barras
        numero_bloco = visionAlgo.getCode(object)
    else: #bloco colorido
        numero_bloco = bloco_escolhido[0]

    print(numero_bloco)

    if numero_bloco == 0: #caso seja o cubo 0, sinaliza só subindo e descendo a garra da frente
        garra.subir_garra_frente(object, 1)
        garra.subir_garra_frente(object, 3)
        garra.subir_garra_frente(object, 2)
        return


    if object.cubo_garra_frente[0] == 0: #garra da frente está vazia
        garra.descer_garra_frente(object)

        #Alinhar o robo com o cubo
        dist_esq_inicial = sensor.le_distancia_ir(object, object.ir_frente_esquerda)
        dist_dir_inicial = sensor.le_distancia_ir(object, object.ir_frente_direita)

        if dist_esq_inicial < dist_dir_inicial: #se o robo estiver à direita do cubo
            cubo = sensor.getCubeHandle(object, object.ir_frente_esquerda) #pega a handle do cubo
            motor.andar_livre(object, -1, 1) #andar para a esquerda
            while True:
                dist_esq = sensor.le_distancia_ir(object, object.ir_frente_esquerda)
                if dist_esq > (dist_esq_inicial + 0.06):
                    motor.stop(object)
                    break
        else: #se o robo estiver à esquerda do cubo
            cubo = sensor.getCubeHandle(object, object.ir_frente_direita) #pega a handle do cubo
            motor.andar_livre(object, 1, 1) #andar para a direita
            while True:
                dist_dir = sensor.le_distancia_ir(object, object.ir_frente_direita)
                if dist_dir > (dist_dir_inicial + 0.06):
                    motor.stop(object)
                    break
    
        #Andar para frente e pegar o cubo
        dist_esq_inicial = sensor.le_distancia_ir(object, object.ir_frente_esquerda)
        dist_dir_inicial = sensor.le_distancia_ir(object, object.ir_frente_direita)
        distancia_cubo = min(dist_dir_inicial, dist_esq_inicial) #distância do robo até o cubo

        garra.abrir_garra_frente(object)
        motor.andar_em_metros(object, 'frente', 1, distancia_cubo+0.025)
        garra.fechar_garra_frente_cubo(object, cubo)
        garra.subir_garra_frente(object, 2)
        object.cubo_garra_frente[0] = numero_bloco #define qual o número do cubo que esta garra está carregando
        object.cubo_garra_frente[1] = cubo #define a handle do cubo que esta garra está carregando


                    
    elif object.cubo_garra_costas[0] == 0: #garra de trás está vazia
        girar.girar_180_graus(object)
        #Realinhar após o giro para garantir que não está torto
        if posicao_cubo == 'esquerda':
            posicao_cubo = 'direita' #como o robo girou, esquerda troca com a direita
            motor.andar_em_metros(object, 'esquerda', 2, 0.05) #garantir que o robo vai estar dentro do quadrado certo para alinhar depois
        elif posicao_cubo == 'direita':
            posicao_cubo = 'esquerda'#como o robo girou, direita troca com a esquerda
            motor.andar_em_metros(object, 'direita', 2, 0.05) #garantir que o robo vai estar dentro do quadrado certo para alinhar depois
        motor.alinharLateral(object, posicao_cubo) #alinhou
    
        garra.descer_garra_costas(object)

        #Como o robo está de costas, quando for andar vai inverter direita e esquerda no argumento da função andar_livre
        #Alinhar o robo com o cubo
        dist_esq_inicial = sensor.le_distancia_ir(object, object.ir_costas_esquerda)
        dist_dir_inicial = sensor.le_distancia_ir(object, object.ir_costas_direita)

        if dist_esq_inicial < dist_dir_inicial: #se o robo estiver à direita do cubo
            cubo = sensor.getCubeHandle(object, object.ir_costas_esquerda) #pega a handle do cubo
            motor.andar_livre(object, 1, 1) #andar para a direita(inverso da esquerda, pois está de costas)
            while True:
                dist_esq = sensor.le_distancia_ir(object, object.ir_costas_esquerda)
                if dist_esq > (dist_esq_inicial + 0.06):
                    motor.stop(object)
                    break
        else: #se o robo estiver à esquerda do cubo
            cubo = sensor.getCubeHandle(object, object.ir_costas_direita) #pega a handle do cubo
            motor.andar_livre(object, -1, 1) #andar para a esquerda(inverso da direita, pois está de costas)
            while True:
                dist_dir = sensor.le_distancia_ir(object, object.ir_costas_direita)
                if dist_dir > (dist_dir_inicial + 0.06):
                    motor.stop(object)
                    break
        
        #Andar para frente e pegar o cubo
        dist_esq_inicial = sensor.le_distancia_ir(object, object.ir_costas_esquerda)
        dist_dir_inicial = sensor.le_distancia_ir(object, object.ir_costas_direita)
        distancia_cubo = min(dist_dir_inicial, dist_esq_inicial) #distância do robo até o cubo

        garra.abrir_garra_costas(object)
        motor.andar_em_metros(object, 'tras', 1, distancia_cubo+0.025) #andar para tras(inverso da frente, pois está de costas)
        garra.fechar_garra_costas_cubo(object, cubo)
        garra.subir_garra_costas(object, 2)
        object.cubo_garra_costas[0] = numero_bloco #define qual o número do cubo que esta garra está carregando
        object.cubo_garra_costas[1] = cubo #define a handle do cubo que esta garra está carregando

def aproximar_prateleira(object, frente_ou_costas):
    if frente_ou_costas == 'frente':
        dist_esq_inicial = sensor.le_distancia_ir(object, object.ir_frente_esquerda)
        dist_dir_inicial = sensor.le_distancia_ir(object, object.ir_frente_direita)
        if dist_esq_inicial > dist_dir_inicial:
            motor.move_frente(object, 2)
            while True:
                dist_esq = sensor.le_distancia_ir(object, object.ir_frente_esquerda)
                if dist_esq < 0.07:
                    break
            motor.stop(object)

        elif dist_dir_inicial > dist_esq_inicial:
            motor.move_frente(object, 2)
            while True:
                dist_dir = sensor.le_distancia_ir(object, object.ir_frente_direita)
                if dist_dir < 0.07:
                    break
            motor.stop(object)

    elif frente_ou_costas == 'costas':
        dist_esq_inicial = sensor.le_distancia_ir(object, object.ir_costas_esquerda)
        dist_dir_inicial = sensor.le_distancia_ir(object, object.ir_costas_direita)
        if dist_esq_inicial > dist_dir_inicial:
            motor.move_tras(object, 2)
            while True:
                dist_esq = sensor.le_distancia_ir(object, object.ir_costas_esquerda)
                if dist_esq < 0.07:
                    break
            motor.stop(object)
            
        elif dist_dir_inicial > dist_esq_inicial:
            motor.move_tras(object, 2)
            while True:
                dist_dir = sensor.le_distancia_ir(object, object.ir_costas_direita)
                if dist_dir < 0.07:
                    break
            motor.stop(object)