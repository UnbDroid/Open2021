import sim
import numpy as np
import time
import simConst
from girar import *
from sensor import *
from motor import *
from object_handle import *

axisX = 0
axisY = 1

############### LÓGICA E FUNÇÕES PARA QUE O ROBÔ ANDE POR QUADRADO ############################


def corrigindoADirecao(object, minhaDirecao, direcaoFinal): #corrige a direção do robô baseado na direção final.
    if(direcaoFinal == NORTE):
        if(minhaDirecao == NORTE):
            return NORTE
        else:
            if(minhaDirecao == LESTE):
                girar_90_graus(object, -1)  # sentido anti horário

            if(minhaDirecao == OESTE):
                girar_90_graus(object, 1)  # sentido horário

            if(minhaDirecao == SUL):
                girar_180_graus(object)
        return direcaoFinal

    if(direcaoFinal == SUL):
        if(minhaDirecao == SUL):
            return SUL
        else:
            if(minhaDirecao == LESTE):
                girar_90_graus(object, 1)  # sentido horário

            if(minhaDirecao == OESTE):
                girar_90_graus(object, -1)  # anti horário

            if(minhaDirecao == NORTE):
                girar_180_graus(object)
        return direcaoFinal

    if(direcaoFinal == LESTE):
        if(minhaDirecao == LESTE):
            return LESTE
        else:
            if(minhaDirecao == OESTE):
                girar_180_graus(object)
            if(minhaDirecao == NORTE):
                girar_90_graus(object, 1)  # sentido horário
            if(minhaDirecao == SUL):
                girar_90_graus(object, -1)  # anti horário
        return direcaoFinal

    if(direcaoFinal == OESTE):
        if(minhaDirecao == OESTE):
            return OESTE
        else:
            if(minhaDirecao == LESTE):
                girar_180_graus(object)
            if(minhaDirecao == NORTE):
                girar_90_graus(object, -1)  # anti horário
            if(minhaDirecao == SUL):
                girar_90_graus(object, 1)  # horário
        return direcaoFinal

def chegadaNolocal(posicaoAtual, posicaoFinal):  #define se chegou ao local
    locaisDeEstoque = [32, 33, 35, 36, 42, 43, 45, 46]
    locaisDeEntrega = [71, 72, 73, 74, 75, 76, 77]
    prateleira = [14]  # média entre as pratileiras

    if(posicaoAtual == posicaoFinal):
        return True

    # O destino final não é o quadrante em si, mas um em volta dele.
    if(posicaoFinal in locaisDeEstoque):
        minDistance = abs(posicaoFinal - posicaoAtual)
        # checa se está a um quadrado de distância apenas.
        if(minDistance == 10 or minDistance == 1):
            return True

    if(posicaoFinal in locaisDeEntrega):  # irá checar se ja está no local.
        if(posicaoAtual == posicaoFinal - 10):
            return True

    # irá checar se ja está 1 quadrado antes da prateleira, para evitar que bata na prateleira.
    if(posicaoFinal in prateleira):
        if(posicaoAtual == posicaoFinal + 10):
            return True

    return False

def IndoDeA_para_B(object, posicaoAtual,  posicaoFinal, minhaDirecao, direcaoFinal): #faz com que o robô ande de A para B, sendo baseado nas posições da arena.

    if minhaDirecao != SUL:
        minhaDirecao = corrigindoADirecao(object,minhaDirecao,SUL)

    while(not chegadaNolocal(posicaoAtual, posicaoFinal)):
        moverY = (int(posicaoFinal/10)) - (int(posicaoAtual/10))
        moverX = (posicaoFinal % 10) - (posicaoAtual % 10)

        if(moverX != 0 and naoLocalDeCarga(object, posicaoAtual, moverX, axisX)):
            print('entrei no if')
            #minhaDirecao = direcaoCorreta(object, minhaDirecao, moverX, axisX, True)

            # O eixo x é a linha horizontal e verifica se ele vai para esquerda ou para direita.
            if(moverX > 0):
                # print("ESSSSSSSSSSQUERDAAAAAAAAA")
                # anda para a esquerda
                moverLadoPorQuadrado(object, 'esquerda')
                posicaoAtual += 1
            else:
                # print("DIIIIIIIIIIREIIIIIIIIIITAAAAAAA")
                moverLadoPorQuadrado(object, 'direita')  # anda para a direita
                posicaoAtual -= 1
        elif(moverY != 0 and naoLocalDeCarga(object, posicaoAtual, moverY, axisY)):
            print('Entrei 1 Elif')
            # minhaDirecao = direcaoCorreta(
            #     object, minhaDirecao, moverX, axisX, True)
            # moverParaFrentePorQuadrado(object)
            if(moverY < 0):  # robô anda para cima
                moverPorQuadrado(object, 'tras')
                posicaoAtual -= 10
            # robô anda para baixo (necessário que ele gire 180 para não ter erro no alinhamento)
            else:
                moverPorQuadrado(object, 'frente')
                posicaoAtual += 10
        else:
            posicaoAtual, minhaDirecao = desvioAreaDeCarga(object,posicaoAtual, posicaoFinal,minhaDirecao,direcaoFinal)

        print(posicaoAtual, moverX, moverY)
        # posicaoAtual, minhaDirecao
    return posicaoAtual, minhaDirecao

def desvioAreaDeCarga(object, posicaoAtual, posicaoFinal, minhaDirecao, direcaoFinal):
    # Parte de cima
    if(int(posicaoAtual/10) == 2):
        destino = posicaoAtual+10
    elif(int(posicaoAtual/10) == 5):
        destino = posicaoAtual-10

    if(posicaoAtual in [22, 25, 52, 55]):
        destino -= 1
    elif(posicaoAtual in [23, 26, 53, 56]):
        destino += 1
    elif(posicaoAtual in [41, 44, 47]):
        destino = posicaoAtual+10
    elif(posicaoAtual in [31, 34, 37]):
        destino = posicaoAtual-10

    posicaoAtual, minhaDirecao = IndoDeA_para_B(object,posicaoAtual, destino,minhaDirecao,direcaoFinal)
    return  posicaoAtual, minhaDirecao

def naoLocalDeCarga(object, posicaoAtual, movement, axis):
    if(axis == axisY):
        if(movement > 0):  # Quer ir pra baixo (SUL)
            # Lista de lugares que não podem ir pra baixo por conta do local de carga
            locaisDeCarga = [22, 23, 25, 26]
        if(movement < 0):  # Quer ir pra cima (NORTE)
            locaisDeCarga = [52, 53, 55, 56]
    if(axis == axisX):
        if(movement > 0):  # Quer ir pra esquerda (LESTE)
            locaisDeCarga = [31, 41, 34, 44]
        if(movement < 0):  # Quer ir pra direita (OESTE)
            locaisDeCarga = [34, 44, 37, 47]
    if(posicaoAtual in locaisDeCarga):
        return False
    return True
   
def entregandoCubos(object, posicaoAtual, posicaoFinal, minhaDirecao, direcaoFinal): 

    Prateleira1 = [11, 6, 1]
    Prateleira2 = [12, 7, 2]
    Prateleira3 = [13, 8, 3]
    Prateleira4 = [14, 9, 4]
    Prateleira5 = [15, 10, 5]
    locaisDeEntrega = [71, 72, 73, 74, 75, 76, 77]
    valGarraFrente = object.cubo_garra_frente
    valGarraCostas = object.cubo_garra_costas

    if valGarraFrente and valGarraCostas != 0:
        if (valGarraFrente in Prateleira1):
            posicaoFinal = 22
            direcaoFinal = NORTE
            IndoDeA_para_B(object, posicaoAtual, posicaoFinal, minhaDirecao, direcaoFinal)
            object.cubo_garra_frente = 0
        elif (valGarraFrente in Prateleira2):
            posicaoFinal = 23
            direcaoFinal = NORTE
            IndoDeA_para_B(object, posicaoAtual, posicaoFinal, minhaDirecao, direcaoFinal)
            object.cubo_garra_frente = 0
        elif (valGarraFrente in Prateleira3):
            posicaoFinal = 24
            direcaoFinal = NORTE
            IndoDeA_para_B(object, posicaoAtual, posicaoFinal, minhaDirecao, direcaoFinal)
            object.cubo_garra_frente = 0
        elif (valGarraFrente in Prateleira4):
            posicaoFinal = 25
            direcaoFinal = NORTE
            IndoDeA_para_B(object, posicaoAtual, posicaoFinal, minhaDirecao, direcaoFinal)
            object.cubo_garra_frente = 0
        elif (valGarraFrente in Prateleira5):
            posicaoFinal = 26
            direcaoFinal = NORTE
            IndoDeA_para_B(object, posicaoAtual, posicaoFinal, minhaDirecao, direcaoFinal)
            object.cubo_garra_frente = 0

        if (valGarraCostas in Prateleira1):
            posicaoFinal = 22
            direcaoFinal = NORTE
            IndoDeA_para_B(object, posicaoAtual, posicaoFinal, minhaDirecao, direcaoFinal)
            object.cubo_garra_costas = 0
        elif (valGarraCostas in Prateleira2):
            posicaoFinal = 23
            direcaoFinal = NORTE
            IndoDeA_para_B(object, posicaoAtual, posicaoFinal, minhaDirecao, direcaoFinal)
            object.cubo_garra_costas = 0
        elif (valGarraCostas in Prateleira3):
            posicaoFinal = 24
            direcaoFinal = NORTE
            IndoDeA_para_B(object, posicaoAtual, posicaoFinal, minhaDirecao, direcaoFinal)
            object.cubo_garra_costas = 0
        elif (valGarraCostas in Prateleira4):
            posicaoFinal = 25
            direcaoFinal = NORTE
            IndoDeA_para_B(object, posicaoAtual, posicaoFinal, minhaDirecao, direcaoFinal)
            object.cubo_garra_costas = 0
        elif (valGarraCostas in Prateleira5):
            posicaoFinal = 26
            direcaoFinal = NORTE
            IndoDeA_para_B(object, posicaoAtual, posicaoFinal, minhaDirecao, direcaoFinal)
            object.cubo_garra_costas = 0
            
    #print(valGarraFrente, valGarraCostas)

# 31, 34, 37, 41, 44 e 47 --> o robô deverá fazer a subtração da sua posição atual pela sua posição final. 
#Caso essa subtração seja < que 10, ele irá subir um quadrado e retomar para a função principal. Atualiza a posição inicial com a final após andar 1 quadrado para cima.
#Caso essa subtração seja > que 10, o robô irá duas casas para baixo e retomará para o código principal. Atualiza a posição inicial com a final após andar 2 quadrado para baixo.

# 22, 23, 25, 26, 52, 53, 55, e 56 --> o robô irá dar a volta pela diagonal
