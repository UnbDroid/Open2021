import sim
import numpy as np
import time
import simConst
from girar import *
from sensor import *
from motor import *
from object_handle import *


#Lógica e funções de andar por quadrado #######

def corrigindoADirecao(object, minhaDirecao, direcaoFinal):
    if(direcaoFinal == NORTE):
        if(minhaDirecao == NORTE):
            return NORTE
        else:
            if(minhaDirecao == LESTE):
                girar_90_graus(object, 1)

            if(minhaDirecao == OESTE):
                girar_90_graus(object, -1)

            if(minhaDirecao == SUL):
                girar_180_graus(object)
        return direcaoFinal

    if(direcaoFinal == SUL):
        if(minhaDirecao == SUL):
            return SUL
        else:
            if(minhaDirecao == LESTE):
                girar_90_graus(object, -1)

            if(minhaDirecao == OESTE):
                girar_90_graus(object, 1)

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
                girar_90_graus(object, 1)
            if(minhaDirecao == SUL):
                girar_90_graus(object, -1)
        return direcaoFinal

    if(direcaoFinal == OESTE):
        if(minhaDirecao == OESTE):
            return OESTE
        else:
            if(minhaDirecao == LESTE):
                girar_180_graus(object)
            if(minhaDirecao == NORTE):
                girar_90_graus(object, 1)
            if(minhaDirecao == SUL):
                girar_90_graus(object, -1)
        return direcaoFinal


def chegadaNolocal(posicaoAtual, posicaoFinal):  # Define se chegou ao local
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


def IndoDeA_para_B(object, posicaoAtual,  posicaoFinal, minhaDirecao, direcaoFinal):
    
    while(not chegadaNolocal(posicaoAtual, posicaoFinal)):
        moverY = (int(posicaoFinal/10)) - (int(posicaoAtual/10))
        moverX = (posicaoFinal % 10) - (posicaoAtual % 10)

        if(moverX != 0):  # and notStockLocal(object, posicaoAtual, moverX, axisX)
            print('entrei no if')
            #minhaDirecao = direcaoCorreta(object, minhaDirecao, moverX, axisX, True)

            # O eixo x é a linha horizontal e verifica se ele vai para esquerda ou para direita.
            if(moverX > 0):
                # print("ESSSSSSSSSSQUERDAAAAAAAAA")
                andarEsquerdaPorQuadrado(object, 'esquerda')  # anda para a esquerda
                posicaoAtual += 1
            else:
                # print("DIIIIIIIIIIREIIIIIIIIIITAAAAAAA")
                andarDireitaPorQuadrado(object, 'direita')  # anda para a direita
                posicaoAtual -= 1
        elif(moverY != 0):  # and notStockLocal(object, posicaoAtual, moverX, axisX)
            print('Entrei 1 Elif')
            # minhaDirecao = direcaoCorreta(
            #     object, minhaDirecao, moverX, axisX, True)
            # moverParaFrentePorQuadrado(object)
            if(moverY < 0):  # robô anda para cima

                moverParaTrasPorQuadrado(object, 'tras')
                posicaoAtual -= 10
            # robô anda para baixo (necessário que ele gire 180 para não ter erro no alinhamento)
            else:
                moverParaFrentePorQuadrado(object, 'frente')
                posicaoAtual += 10

        print(posicaoAtual, moverX, moverY)
        # posicaoAtual, minhaDirecao
    return corrigindoADirecao(object,minhaDirecao,direcaoFinal)


# def desvioAreaDeCarga(object, posicaoAtual, minhaDirecao):
    # Parte de cima
    if(posicaoAtual == 22):
        minhaDirecao = direcaoCorreta(object, minhaDirecao, -1, axisY, True)
        moverParaFrentePorQuadrado(object)
        minhaDirecao = direcaoCorreta(object, minhaDirecao, +1, axisX, True)
        moverParaFrentePorQuadrado(object)
        posicaoAtual = 31
    if(posicaoAtual == 23):
        minhaDirecao = direcaoCorreta(object, minhaDirecao, +1, axisY, True)
        moverParaFrentePorQuadrado(object)
        minhaDirecao = direcaoCorreta(object, minhaDirecao, +1, axisX, True)
        moverParaFrentePorQuadrado(object)
        posicaoAtual = 34
    if(posicaoAtual == 25):
        minhaDirecao = direcaoCorreta(object, minhaDirecao, -1, axisY, True)
        moverParaFrentePorQuadrado(object)
        minhaDirecao = direcaoCorreta(object, minhaDirecao, +1, axisX, True)
        moverParaFrentePorQuadrado(object)
        posicaoAtual = 34
    if(posicaoAtual == 26):
        minhaDirecao = direcaoCorreta(object, minhaDirecao, +1, axisY, True)
        moverParaFrentePorQuadrado(object)
        minhaDirecao = direcaoCorreta(object, minhaDirecao, +1, axisX, True)
        moverParaFrentePorQuadrado(object)
        posicaoAtual = 37
    # Parte de baixo
    if(posicaoAtual == 52):
        minhaDirecao = turnTo(object, minhaDirecao, OESTE, True)
        moverParaFrentePorQuadrado(object)
        minhaDirecao = turnTo(object, minhaDirecao, NORTE, True)
        moverParaFrentePorQuadrado(object)
        posicaoAtual = 41
    if(posicaoAtual == 53):
        minhaDirecao = turnTo(object, minhaDirecao, LESTE, True)
        moverParaFrentePorQuadrado(object)
        minhaDirecao = turnTo(object, minhaDirecao, NORTE, True)
        moverParaFrentePorQuadrado(object)
        posicaoAtual = 44
    if(posicaoAtual == 55):
        minhaDirecao = turnTo(object, minhaDirecao, OESTE, True)
        moverParaFrentePorQuadrado(object)
        minhaDirecao = turnTo(object, minhaDirecao, NORTE, True)
        moverParaFrentePorQuadrado(object)
        posicaoAtual = 44
    if(posicaoAtual == 56):
        minhaDirecao = turnTo(object, minhaDirecao, LESTE, True)
        moverParaFrentePorQuadrado(object)
        minhaDirecao = turnTo(minhaDirecao, NORTE, True)
        moverParaFrentePorQuadrado(object)
        posicaoAtual = 47
    print(posicaoAtual, minhaDirecao)
    return posicaoAtual, minhaDirecao

# def notStockLocal(object, posicaoAtual, movement, axis):
    if(axis == axisX):
        if(movement > 0):  # Quer ir pra baixo (SUL)
            # Lista de lugares que não podem ir pra baixo por conta do local de carga
            locaisDeCarga = [22, 23, 25, 26]
        if(movement < 0):  # Quer ir pra cima (NORTE)
            locaisDeCarga = [52, 53, 55, 56]
    if(axis == axisY):
        if(movement > 0):  # Quer ir pra esquerda (LESTE)
            locaisDeCarga = [31, 41, 34, 44]
        if(movement < 0):  # Quer ir pra direita (OESTE)
            locaisDeCarga = [34, 44, 37, 47]
    if(posicaoAtual in locaisDeCarga):
        return False
    return True