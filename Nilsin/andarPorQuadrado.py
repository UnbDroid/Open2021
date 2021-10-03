import sim
import numpy as np
import time
import simConst
from girar import *
from sensor import *
from motor import *
from object_handle import *


#Lógica e funções de andar por quadrado #######

def corrigindoADirecao(object,minhaDirecao, direcaoFinal):
    if(direcaoFinal == NORTE):
        if(minhaDirecao == NORTE):
            return NORTE
        else:
            if(minhaDirecao == LESTE):
                #girar90
                return minhaDirecao
            if(minhaDirecao == OESTE):
                #girar-90
                return minhaDirecao
            if(minhaDirecao == SUL):
                #girar-180
                return minhaDirecao
    if(direcaoFinal == SUL):
        if(minhaDirecao == SUL):
            return SUL
        else:
            if(minhaDirecao == LESTE):
                #girar-90
                return minhaDirecao
            if(minhaDirecao == OESTE):
                #girar90
                return minhaDirecao
            if(minhaDirecao == NORTE):
                #girar180
                return minhaDirecao
    if(direcaoFinal == LESTE):
        if(minhaDirecao == LESTE):
            return LESTE
        else:
            if(minhaDirecao == OESTE):
                #girar-180
                return minhaDirecao
            if(minhaDirecao == NORTE):
                #girar90
                return minhaDirecao
            if(minhaDirecao == SUL):
                #girar-90
                return minhaDirecao
    if(direcaoFinal == OESTE):
        if(minhaDirecao == OESTE):
            return OESTE
        else:
            if(minhaDirecao == LESTE):
                #girar-180
                return minhaDirecao
            if(minhaDirecao == NORTE):
                #girar90
                return minhaDirecao
            if(minhaDirecao == SUL):
                #girar-90
                return minhaDirecao
           

def chegadaNolocal(posicaoAtual, posicaoFinal):  # Define se chegou ao local
    locaisDeEstoque = [32, 33, 35, 36, 42, 43, 45, 46]
    locaisDeEntrega = [71, 72, 73, 74, 75, 76, 77]
    prateleira = [14]  # média entre as pratileiras

    if(posicaoAtual == posicaoFinal):
        return True

    if(posicaoFinal in locaisDeEstoque):  # O destino final não é o quadrante em si, mas um em volta dele.
        minDistance = abs(posicaoFinal - posicaoAtual)
        if(minDistance == 10 or minDistance == 1):  # checa se está a um quadrado de distância apenas.
            return True 

    if(posicaoFinal in locaisDeEntrega): #irá checar se ja está no local.
        if(posicaoAtual == posicaoFinal - 10):
            return True
            
    if(posicaoFinal in prateleira): #irá checar se ja está 1 quadrado antes da prateleira, para evitar que bata na prateleira.
        if(posicaoAtual == posicaoFinal + 10):
            return True

    return False
    

def IndoDeA_para_B(object, posicaoAtual,  posicaoFinal, minhaDirecao):
    while(not chegadaNolocal(posicaoAtual, posicaoFinal)):
        moverY = (int(posicaoFinal/10)) - (int(posicaoAtual/10))
        moverX = (posicaoFinal % 10) - (posicaoAtual % 10)
        
        if(moverX != 0): # and notStockLocal(object, posicaoAtual, moverX, axisX)
            print('entrei no if')
            #minhaDirecao = direcaoCorreta(object, minhaDirecao, moverX, axisX, True)

            if(moverX > 0): # O eixo x é a linha horizontal e verifica se ele vai para esquerda ou para direita.
                andarParaOLadoPorQuadrado(object, 6) # anda para a direita
                posicaoAtual += 1
            else: 
                andarParaOLadoPorQuadrado(object, 4) # anda para a esquerda
                posicaoAtual -= 1
        elif(moverY != 0): #and notStockLocal(object, posicaoAtual, moverX, axisX)
            print('Entrei 1 Elif')
            # minhaDirecao = direcaoCorreta(
            #     object, minhaDirecao, moverX, axisX, True)
            # moverParaFrentePorQuadrado(object)
            if(moverY < 0):  # robô anda para cima
                moverParaFrentePorQuadrado(object, 8)
                posicaoAtual -= 10
            else:  # robô anda para baixo (necessário que ele gire 180 para não ter erro no alinhamento)
                moverParaFrentePorQuadrado(object, 2)
                posicaoAtual += 10
        print(posicaoAtual, moverX, moverY)
    return posicaoAtual, minhaDirecao
            
            
        


