import time
import sys
#from graphb
from garra import *
from girar import *
from motor import *
from sensor import *
from object_handle import ObjectHandle
from andarPorQuadrado import *
import visionAlgo
from logLocomAlgo import *
from algoritmo import *

try:
    import sim
except:
    print('--------------------------------------------------------------')
    print('"sim.py" could not be imported. This means very probably that')
    print('either "sim.py" or the remoteApi library could not be found.')
    print('Make sure both are in the same folder as this file,')
    print('or appropriately adjust the file "sim.py"')
    print('--------------------------------------------------------------')
    print('')

sim.simxFinish(-1)  # just in case, close all opened connections
global clientID
clientID = sim.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
robotname = 'S_Base'


if clientID != -1:
    sim.simxStartSimulation(clientID, sim.simx_opmode_oneshot_wait)
    print('Connected to remote API server')
    sim.simxAddStatusbarMessage(clientID, 'Funcionando...', sim.simx_opmode_oneshot_wait)
    time.sleep(0.02)
    adeni = ObjectHandle(clientID, robotname) #instancia objeto
    #IndoDeA_para_B(adeni,31,34,SUL,SUL)


    def firstAreaCubes(currentPosition, myDirection, order):
        if(order == 1):
            destine = 22
            direction = LESTE
            lastTurn = 1
        if(order == 2):
            destine = 23
            direction = OESTE
            lastTurn = -1
        #Vai para a primeira área
        currentPosition, myDirection = IndoDeA_para_B(adeni,currentPosition, destine, myDirection,direction)
        print("parei")
        #Se posiciona da melhor forma para enxergar os blocos
        #Align() #TurnTo ja alinha
        andar_em_metros(adeni,'frente', 2, 0.08)
        andar_em_metros(adeni,'tras',2, 0.065)
        matrix0 = visionAlgo.resolveVision(adeni,0)
        #time.sleep(3)
        return matrix0, currentPosition, myDirection



    def secondAreaCubes(currentPosition, myDirection, order):
    #Vai para a segunda área
    # myDirection = turnTo(myDirection ,EAST)
    # #MoveDirectionPosition(frente, 0.020)
    # currentPosition += 1
        print('segunda')
        if(order == 2):
            destine = 25
            direction = LESTE
            lastTurn = 1
        if(order == 1):
            destine = 26
            direction = OESTE
            lastTurn = -1
        currentPosition, myDirection = IndoDeA_para_B(adeni,currentPosition, destine, myDirection,direction)
        #Se posiciona da melhor forma para enxergar os blocos
        #Align()
        andar_em_metros(adeni, 'frente', 2, 0.08)
        andar_em_metros(adeni,'tras' ,2, 0.065)
        matrix1 = visionAlgo.resolveVision(adeni,1)
        return matrix1, currentPosition, myDirection

    def thirdAreaCubes(currentPosition, myDirection, order):
        print('terceira')
        if(order == 1):
            destine = 52
            direction = LESTE
            lastTurn = -1
        if(order == 2):
            destine = 53
            direction = OESTE
            lastTurn = 1
        #Vai para a primeira área
        print(destine)
        currentPosition, myDirection = IndoDeA_para_B(adeni,currentPosition, destine, myDirection,myDirection)
        #Se posiciona da melhor forma para enxergar os blocos
        myDirection = corrigindoADirecao(adeni ,myDirection,direction)
        #Align() #TurnTo ja alinha
        andar_em_metros(adeni,'frente', 2, 0.08)
        girar_90_graus(adeni,lastTurn)
        myDirection = NORTE
        #align.Align()
        andar_em_metros(adeni,'tras',2, 0.065)
        print('ta aqui o erro')
        matrix0 = visionAlgo.resolveVision(adeni,0) ####ALTERAR A MATRIZ
        matrix0 = invertMatrix(matrix0)
        #time.sleep(3)
        print('nao sai')
        return matrix0, currentPosition, myDirection
    def fourthAreaCubes(currentPosition, myDirection, order):
        print('quarta')
        #Vai para a segunda área
        # myDirection = turnTo(myDirection ,EAST)
        # #MoveDirectionPosition(frente, 0.020)
        # currentPosition += 1
        if(order == 2):
            destine = 55
            direction = LESTE
            lastTurn = -1
        if(order == 1):
            destine = 56
            direction = OESTE
            lastTurn = 1
        currentPosition, myDirection = IndoDeA_para_B(adeni,currentPosition, destine, myDirection, myDirection)
        #Se posiciona da melhor forma para enxergar os blocos
        myDirection = corrigindoADirecao(adeni ,myDirection,direction)
        #Align()
        andar_em_metros(adeni,'frente', 2, 0.08)
        girar_90_graus(adeni,lastTurn)
        myDirection = NORTE
        #align.Align()
        andar_em_metros(adeni,'tras',2, 0.065)
        matrix1 = visionAlgo.resolveVision(adeni,1) #MODIFICAR MATRIZ
        matrix1 = invertMatrix(matrix1)
        return matrix1, currentPosition, myDirection



    def getBlocksInformation(currentPosition, myDirection):
        print(currentPosition)
        print('get block information')
        if (currentPosition < 40): #Ta na parte de cima
            if(currentPosition % 10 <= 2):
                print("Primeira área1")
                time.sleep(2)
                matrix0, currentPosition, myDirection = firstAreaCubes(currentPosition, myDirection, 1)
                #Vai para a segunda área
                print("Segunda área1")
                time.sleep(2)
                #MoveDirectionPosition(frente, 0.020)
                currentPosition += 1
                matrix1, currentPosition, myDirection = secondAreaCubes(currentPosition, myDirection, 2)
            elif(currentPosition % 10 <= 4):
                print("Primeira área2")
                time.sleep(2)
                matrix0, currentPosition, myDirection = firstAreaCubes(currentPosition, myDirection, 2)
                #Vai para a segunda área
                print("Segunda área2")
                time.sleep(2)
                #MoveDirectionPosition(frente, 0.020)
                matrix1, currentPosition, myDirection = secondAreaCubes(currentPosition, myDirection, 2)
            else:
                print("Primeira área3")
                time.sleep(2)
                matrix1, currentPosition, myDirection = secondAreaCubes(currentPosition, myDirection, 1)

                print("Segunda área3")
                time.sleep(2)
                currentPosition -= 1
                matrix0, currentPosition, myDirection = firstAreaCubes(currentPosition, myDirection, 2)
        else: #Ta na parte de baixo
            if(currentPosition % 10 <= 2):
                matrix0, currentPosition, myDirection = thirdAreaCubes(currentPosition, myDirection, 1)
                #Vai para a segunda área
                myDirection = corrigindoADirecao(adeni,myDirection ,LESTE)
                #MoveDirectionPosition(frente, 0.020)
                currentPosition += 1
                matrix1, currentPosition, myDirection = fourthAreaCubes(currentPosition, myDirection, 2)
            elif(currentPosition % 10 <= 4):
                matrix0, currentPosition, myDirection = thirdAreaCubes(currentPosition, myDirection, 2)
                #Vai para a segunda área
                myDirection = corrigindoADirecao(adeni,myDirection ,LESTE)
                #MoveDirectionPosition(frente, 0.020)
                matrix1, currentPosition, myDirection = fourthAreaCubes(currentPosition, myDirection, 2)
            else:
                matrix1, currentPosition, myDirection = fourthAreaCubes(currentPosition, myDirection, 1)
                myDirection = corrigindoADirecao(adeni,myDirection ,OESTE)
                currentPosition -= 1
                matrix0, currentPosition, myDirection = thirdAreaCubes(currentPosition, myDirection, 2)

        #time.sleep(3)

        #myDirection = turnTo(myDirection ,WEST)
        #MoveDirectionPosition(frente, 0.020)
        #currentPosition += 1
        # print(matrix0)
        # print(matrix1)
        matrix = np.concatenate((matrix0, matrix1), axis=0)

        #order = gb.get_path(gb.createGraphBlocks(matrix))  #AQUI FUNCIONA COM O CODIGO SIMPLES!!!!!
        #print(order, matrixFinal)
        return currentPosition, myDirection, matrix

    def winOPEN():

        initialPosition = [4,1]
        if(initialPosition[1] == -1):
            moverPorQuadrado(adeni,'frente')
            alinhar(adeni, 'frente')
            andar_em_metros(adeni,'frente', 5, 0.065)
        iniY, iniX = 1,3  #TREM DE CV PARA CALCULAR O ALGORITM
        initialPosition = (iniY+1)*10+(iniX+1)
        print(initialPosition, 'win OPEN')
        # VERIFICAR ISSO!!!!!!!!!!!!!! PRA PEGAR DIREÇÃO INICIAL
        initialDirection = SUL
        ##### PARA TESTES ######
        #FIRST AREA:
        #initialPosition = 24
        #SECOND AREA:
        initialPosition = 27
        currentPosition, myDirection, matrix = getBlocksInformation(initialPosition, initialDirection)
        print(matrix, 'DEPOIS DO WIN OPEN')
        #time.sleep(1000)
        #order = [1, 2, 3]
        pickLater = []
        blockZero = []
        #APENAS TESTE
        #order = gb.get_path(gb.createGraphBlocks(matrix))
        #currentPosition = initialPosition
        #myDirection = initialDirection
        #FIM DE TESTE
    winOPEN()

else:
    print('Failed connecting to remote API server')
    sys.exit()
