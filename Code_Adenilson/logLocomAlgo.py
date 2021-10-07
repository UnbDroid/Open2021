# coding=utf-8
# Insert in a script in Coppelia
import time
import sim
from girar import *
from motor import *
from sensor import *
from object_handle import *
from andarPorQuadrado import *
#import alignAlgo as align
#import cuboAlgo as cubo

#### Funções de lógica de movimentação ##############################################


def posicaoRealFinal(object, posicaoFinal):
    locaisDeEstoque = [32, 33, 35, 36, 42, 43, 45, 46]
    locaisDeEntrega = [71, 72, 73, 74, 75, 76, 77]
    prateleira = [14]  # media entre as pratileiras
    if(posicaoFinal in locaisDeEntrega):
        posicaoFinal -= 10
    if(posicaoFinal in prateleira):
        posicaoFinal += 10
    # if(posicaoFinal in locaisDeEstoque) #### Definir o local em que irá pegar o cubo
    return posicaoFinal


def chegadaNolocal(object, posicaoAtual, posicaoFinal):  # Define se chegou ao local
    if(posicaoAtual == posicaoFinal):
        return True
    locaisDeEstoque = [32, 33, 35, 36, 42, 43, 45, 46]
    if(posicaoFinal in locaisDeEstoque):  # O destino final não é o quadrante em si, mas um em volta dele
        minDistance = abs(posicaoFinal - posicaoAtual)
        if(minDistance == 1 or minDistance == 10):  # checa se está a um quadrado de distância apenas
            return True
    return False


# define se o robô está virado para a direção correta, se não, corrige. Retorna direção atual
def direcaoCorreta(object, minhaDirecao, movement, axis, alinhar):
    if(axis == axisX):
        if(movement > 0):  # Quer ir pra baixo (SUL) ###
            if(minhaDirecao == SUL):
                return SUL
            else:
                if(minhaDirecao == NORTE):
                    alinharOuNao(object, 180, alinhar)
                if(minhaDirecao == OESTE):
                    alinharOuNao(object, 90, alinhar)
                if(minhaDirecao == LESTE):
                    alinharOuNao(object, -90, alinhar)
                return SUL
        if(movement < 0):  # Quer ir pra cima (NORTE)
            if(minhaDirecao == NORTE):
                return NORTE
            else:
                if(minhaDirecao == SUL):
                    alinharOuNao(object, 180, alinhar)
                if(minhaDirecao == OESTE):
                    alinharOuNao(object, -90, alinhar)
                if(minhaDirecao == LESTE):
                    alinharOuNao(object, 90, alinhar)
                return NORTE

    if(axis == axisY):
        if(movement > 0):  # Quer ir pra direita (LESTE)
            if(minhaDirecao == LESTE):
                return LESTE
            else:
                if(minhaDirecao == OESTE):
                    alinharOuNao(object, 180, alinhar)
                if(minhaDirecao == NORTE):
                    alinharOuNao(object, -90, alinhar)
                if(minhaDirecao == SUL):
                    alinharOuNao(object, 90, alinhar)
                return LESTE
        if(movement < 0):  # Quer ir pra esquerda (OESTE)
            if(minhaDirecao == OESTE):
                return OESTE
            else:
                if(minhaDirecao == LESTE):
                    alinharOuNao(object, 180, alinhar)
                if(minhaDirecao == NORTE):
                    alinharOuNao(object, 90, alinhar)
                if(minhaDirecao == SUL):
                    alinharOuNao(object, -90, alinhar)
                return OESTE


def alinharOuNao(object, angulo, alinhar):
    if(alinhar):
        TurnInSquare(object, angulo)
    else:
        if(angulo > 0):
            direcaoEGiro(object, abs(angulo))
        if(angulo < 0):
            direcaoEGiro(object, abs(angulo))


def turnTo(object, minhaDirecao, direcaoFinal, alinhar):
    if(direcaoFinal == NORTE):
        if(minhaDirecao == LESTE):
            alinharOuNao(object, 90, alinhar)
        if(minhaDirecao == SUL):
            alinharOuNao(object, 180, alinhar)
        if(minhaDirecao == OESTE):
            alinharOuNao(object, -90, alinhar)
        return NORTE
    if(direcaoFinal == LESTE):
        if(minhaDirecao == NORTE):
            alinharOuNao(object, -90, alinhar)
        if(minhaDirecao == SUL):
            alinharOuNao(object, 90, alinhar)
        if(minhaDirecao == OESTE):
            alinharOuNao(object, 180, alinhar)
        return LESTE
    if(direcaoFinal == SUL):
        if(minhaDirecao == LESTE):
            alinharOuNao(object, -90, alinhar)
        if(minhaDirecao == NORTE):
            alinharOuNao(object, 180, alinhar)
        if(minhaDirecao == OESTE):
            alinharOuNao(object, 90, alinhar)
        return SUL
    if(direcaoFinal == OESTE):
        if(minhaDirecao == LESTE):
            alinharOuNao(object, 180, alinhar)
        if(minhaDirecao == SUL):
            alinharOuNao(object, -90, alinhar)
        if(minhaDirecao == NORTE):
            alinharOuNao(object, 90, alinhar)
        return OESTE


# define se o robô está em volta de uma aŕea de carga onde não pode entrar
def notStockLocal(object, posicaoAtual, movement, axis):
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


# desvia da área de carga e retorna nova posição e direção
def desvioAreaDeCarga(object, posicaoAtual, minhaDirecao):
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


def corrigindoDirecao(object, moverX, moverY, posicaoAtual, minhaDirecao):
    if(moverY != 0 and notStockLocal(object, posicaoAtual, moverY, axisY)):
        minhaDirecao = direcaoCorreta(
            object, minhaDirecao, moverY, axisY, False)
    elif(moverX != 0 and notStockLocal(object, posicaoAtual, moverX, axisX)):
        minhaDirecao = direcaoCorreta(
            object, minhaDirecao, moverX, axisX, False)
    return minhaDirecao


def irMetadeDoQuadrado(object, moverX, moverY, posicaoAtual, minhaDirecao):
    if(moverY != 0 and notStockLocal(object, posicaoAtual, moverY, axisY)):
        minhaDirecao = direcaoCorreta(
            object, minhaDirecao, moverY, axisY, True)
        if(moverY > 0):  # robô andou para a direita
            posicaoAtual += 1
        else:  # robô andou para a esquerda
            posicaoAtual -= 1
    elif(moverX != 0 and notStockLocal(object, posicaoAtual, moverX, axisX)):
        minhaDirecao = direcaoCorreta(
            object, minhaDirecao, moverX, axisX, True)
        if(moverX > 0):  # robô andou para baixo
            posicaoAtual += 10
        else:  # robô andou para cima
            posicaoAtual -= 10
    andar_em_metros(object, 8, 5, 0.15)

    return posicaoAtual, minhaDirecao


# Permite que o robô vá de um canto para o outro.
def deA_para_B(object, posicaoAtual, posicaoFinal, minhaDirecao):
    posicaoFinal = posicaoRealFinal(object, posicaoFinal)
    i = 0
    print("pos final",posicaoAtual)
    print("pos inicial",posicaoFinal)
    while(not chegadaNolocal(object, posicaoAtual, posicaoFinal)):
        moverX = (int(posicaoFinal/10)) - (int(posicaoAtual/10))
        moverY = (posicaoFinal % 10) - (posicaoAtual % 10)
        if(i == 0):
            minhaDirecao = corrigindoDirecao(
                object, moverX, moverY, posicaoAtual, minhaDirecao)
            i += 1
        print
        # otiimização para andar até a metade do quadrado.
        if((abs(moverX) == 1 and abs(moverY) == 0)):
            print('ate metade')
            print(posicaoAtual)
            posicaoAtual, minhaDirecao = irMetadeDoQuadrado(
                object, moverX, moverY, posicaoAtual, minhaDirecao)
            print('sai', posicaoAtual)
        elif(moverY != 0 and notStockLocal(object, posicaoAtual, moverY, axisY)):
            print('Entrei 1 Elif')
            minhaDirecao = direcaoCorreta(
                object, minhaDirecao, moverY, axisY, True)
            moverParaFrentePorQuadrado(object)
            if(moverY > 0):  # robô andou para a direita
                posicaoAtual += 1
            else:  # robô andou para a esquerda
                posicaoAtual -= 1
        elif(moverX != 0 and notStockLocal(object, posicaoAtual, moverX, axisX)):
            print('Entrei 2 Elif')
            minhaDirecao = direcaoCorreta(
                object, minhaDirecao, moverX, axisX, True)
            moverParaFrentePorQuadrado(object)
            if(moverX > 0):  # robô andou para baixo
                posicaoAtual += 10
            else:  # robô andou para cima
                posicaoAtual -= 10
        # o robô ja chegou no eixo Y, mas não pode se movimentar em X por conta da área de carga
        elif (moverY == 0 and not notStockLocal(object, posicaoAtual, moverX, axisX)):
            print('Entrei 3 Elif')
            posicaoAtual, minhaDirecao = desvioAreaDeCarga(
                object, posicaoAtual, minhaDirecao)
        print(posicaoAtual, moverX, moverY)
        time.sleep(1)
    print('sai')
    return posicaoAtual, minhaDirecao

# def posicaoDaPrateleira(block, minhaDirecao): ###
#     if(Prateleiras[block] != 0):
#         alinhamentoComOCubo(minhaDirecao, LESTE, esquerda, False)
#         alinhar()
#         #align.AlignSpecial(2)
#         return NORTE

#     return minhaDirecao

# def entregarNaPrateleira(block, posicaoAtual, minhaDirecao, cube): ###
#     prateleira1 = [1, 6, 11]
#     prateleira2 = [2, 7, 12]
#     prateleira3 = [3, 8, 13]
#     prateleira4 = [4, 9, 14]
#     prateleira5 = [5, 10, 15]
#     if (block in prateleira1):
#         posicaoAtual, minhaDirecao = deA_para_B(posicaoAtual, 22, minhaDirecao)
#     if (block in prateleira2):
#         posicaoAtual, minhaDirecao = deA_para_B(posicaoAtual, 23, minhaDirecao)
#     if (block in prateleira3):
#         posicaoAtual, minhaDirecao = deA_para_B(posicaoAtual, 24, minhaDirecao)
#     if (block in prateleira4):
#         posicaoAtual, minhaDirecao = deA_para_B(posicaoAtual, 25, minhaDirecao)
#     if (block in prateleira5):
#         posicaoAtual, minhaDirecao = deA_para_B(posicaoAtual, 26, minhaDirecao)

#     minhaDirecao = posicaoDaPrateleira(block, minhaDirecao)

#     minhaDirecao = turnTo(minhaDirecao, NORTE, True)

#     #if(block <= 5):
#         #cubo.entregar_cubo_primeiro_andar(cube)
#     #elif(block <= 10):
#         #cubo.entregar_cubo_segundo_andar(cube)
#     #elif(block <= 15):
#         #cubo.entregar_cubo_terceiro_andar(cube)
#     #Prateleiras[block] += 1

#     andar_em_metros(adeni, 2, 3, 0.065)

#     return posicaoAtual, minhaDirecao

# def alinhamentoComOCubo(minhaDirecao, corrigindoDirecao, finalTurn, cuboEscondido): #deixa o robô pronto e alinhado para pegar o cubo desejado.
#     #MoveDirectionPosition(tras, 0.01)
#     if(minhaDirecao == -corrigindoDirecao):
#     #if(False):
#         andar_em_metros(adeni,2, 5, 0.10)
#         alinhar()
#         andar_em_metros(adeni,8, 2, 0.16)
#         direcaoEGiro(-finalTurn, 90)
#     else:
#         print('virando', corrigindoDirecao)
#         turnTo(minhaDirecao, corrigindoDirecao, True)
#         alinhar() #necessário ser um alinhamento mais 'devagar' para garantir que não ocorra erros na horaa de pegar.
#         MoveDirectionPosition(2, 0.002)
#         print('virando', finalTurn)
#         direcaoEGiro(finalTurn, 90)

#     alinhar()
#     if not cuboEscondido:
#         andar_em_metros(adeni,2, 5, 0.06)

    #MoveDirectionPosition(tras, 0.01)
