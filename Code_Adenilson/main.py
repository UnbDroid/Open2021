import time
import sys
#from graphb
from garra import *
from girar import *
from motor import *
from sensor import *
from object_handle import ObjectHandle
from andarPorQuadrado import *
from visionAlgo import *
from cubo import *
from logLocomAlgo import *
from algoritmo import *
import firstSq

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

    # print('Antes:', adeni.cubo_garra_frente)
    # alinhar_e_pegar_cubo(adeni, ['K', 0, 1])
    # print('Depois:', adeni.cubo_garra_frente)

    #IndoDeA_para_B(adeni,31,34,SUL,SUL)


    def firstAreaCubes(currentPosition, myDirection, order):
        velocidade = 3
        acima = [22,23,25,26]
        if(order == 1):
            destine = 22
            lastTurn = 1
            lado = 'esquerda'
        if(order == 2):
            destine = 23
            lastTurn = -1
            lado = 'direita'
        direction = SUL
        # print('*********1',currentPosition, destine, myDirection, direction)
        #Vai para a primeira área
        currentPosition, myDirection = IndoDeA_para_B(adeni,currentPosition, destine, myDirection,direction)

        # print("parei")
        #Se posiciona da melhor forma para enxergar os blocos
        #Align() #TurnTo ja alinha
        alinharLateral(adeni, lado)
        # alinhar(adeni, "tras")
        andar_em_metros(adeni,lado,velocidade,0.12)
        # print(currentPosition)


        #while Ler_Cor(adeni, 'esquerda') == 'BRANCO' and Ler_Cor(adeni, 'direita') =='BRANCO':
         #       move_forward(adeni, 2)
        #if currentPosition not in acima:
         #   while Ler_Cor(adeni, 'esquerda') == 'BRANCO' and Ler_Cor(adeni, 'direita') =='BRANCO':
          #          move_forward(adeni, 2)
        while Ler_Cor(adeni, 'esquerda') == 'BRANCO' and Ler_Cor(adeni, 'direita') =='BRANCO':
            move_forward(adeni, velocidade)
        # while Ler_Cor(adeni, 'esquerda') == 'PRETO' and Ler_Cor(adeni, 'direita') =='PRETO':
        #     move_forward(adeni, 2)
        # while Ler_Cor(adeni, 'esquerda') == 'BRANCO' and Ler_Cor(adeni, 'direita') =='BRANCO':
        #     move_forward(adeni, 2)

        # andar_em_metros(adeni,'tras',2, 0.1)
        alinhar(adeni, "tras")
        #time.sleep(3)
        alinharComLateralFT(adeni, 'tras', 1)
        andar_em_metros(adeni, 'frente', velocidade,0.035)
        matrix0 = visionAlgo.resolveVision(adeni,0)
        andar_em_metros(adeni,'frente',velocidade, 0.05)

        return matrix0, currentPosition, myDirection

    def secondAreaCubes(currentPosition, myDirection, order):
        velocidade = 3
        #Vai para a segunda área
        # myDirection = turnTo(myDirection ,EAST)
        # #MoveDirectionPosition(frente, 0.020)
        # currentPosition += 1
        # print('segunda')
        if(order == 1):
            destine = 25
            lastTurn = 1
            lado ='esquerda'
        if(order == 2):
            destine = 26
            lastTurn = -1
            lado = 'direita'
        direction = SUL
        # print('*********2',currentPosition, destine, myDirection, direction)
        currentPosition, myDirection = IndoDeA_para_B(adeni,currentPosition, destine, myDirection,direction)
        #Se posiciona da melhor forma para enxergar os blocos
        #Align()
        alinharLateral(adeni, lado)
        # alinhar(adeni, "tras")
        andar_em_metros(adeni,lado,velocidade,0.12)
        while Ler_Cor(adeni, 'esquerda') == 'BRANCO ' and Ler_Cor(adeni, 'direita' == 'BRANCO'):
            move_forward(adeni, velocidade)
        # print('sai do while')
        # andar_em_metros(adeni,'tras' ,2, 0.1)
        alinhar(adeni, "tras")
        alinharComLateralFT(adeni, 'tras', 1)
        andar_em_metros(adeni, 'frente', velocidade,0.035)
        matrix1 = visionAlgo.resolveVision(adeni,1)
        andar_em_metros(adeni,'frente',velocidade, 0.05)
        return matrix1, currentPosition, myDirection

    def thirdAreaCubes(currentPosition, myDirection, order):
        velocidade = 3
        # print('terceira')
        if(order == 1):
            destine = 52
            direction = LESTE
            lastTurn = -1
            lado ='esquerda'
        if(order == 2):
            destine = 53
            direction = OESTE
            lastTurn = 1
            lado = 'direita'
        #Vai para a primeira área
        # print(destine)
        currentPosition, myDirection = IndoDeA_para_B(adeni,currentPosition, destine, myDirection,SUL)
        #Se posiciona da melhor forma para enxergar os blocos

        alinharLateral(adeni, lado)
        # while Ler_Cor(adeni, 'esquerda')=='BRANCO' and Ler_Cor(adeni , 'direita')== 'BRANCO':
        #     alinharLateral(adeni, lado)
        #     move_frente(adeni, 2)
        #alinhar(adeni, 'frente')
        andar_em_metros(adeni, lado, velocidade,0.1)
        giroRSEA(adeni, 1)
        #alinhar(adeni, 'frente')
        #alinhar(adeni, 'frente')
        # while Ler_Cor(adeni, 'esquerda')=='BRANCO' and Ler_Cor(adeni , 'direita')== 'BRANCO':
        #     move_frente(adeni, 2)
        #andar_em_metros(adeni, 'frente', 2,0.08)
        alinhar(adeni , 'frente')
        #alinharComLateralFT(adeni, 'frente', -1)
        andar_em_metros(adeni, 'tras', velocidade,0.08)
        alinhar(adeni, 'tras')
        alinharComLateralFT(adeni, 'tras', 1)
        #alinharComLateralFT(adeni, 'tras', -1)

        andar_em_metros(adeni, 'frente', velocidade,0.035)

        #Align() #TurnTo ja alinha
        #andar_em_metros(adeni,'frente', 2, 0.1)
        myDirection = NORTE
        #align.Align()
        # while Ler_Cor(adeni, 'esquerdalateral1')=='BRANCO' and Ler_Cor(adeni , 'direitalateral1')== 'BRANCO':
        #      alinharLateral(adeni, lado)
        #      move_tras(adeni, 2)

        #andar_em_metros(adeni,'tras',2, 0.085)
        # print('ta aqui o erro')
        #giroRSEA(adeni)

        matrix0 = visionAlgo.resolveVision(adeni,0) ####ALTERAR A MATRIZ
        matrix0 = invertMatrix(matrix0)
        #andar_em_metros(adeni, 'frente', 2, 0.04)
        #time.sleep(3)
        # print('nao sai')
        andar_em_metros(adeni,'frente' , velocidade, 0.05)
        andar_em_metros(adeni, lado, velocidade, 0.02) #LINHA NOVA
        return matrix0, currentPosition, myDirection

    def fourthAreaCubes(currentPosition, myDirection, order):
        velocidade = 3
        # print('quarta')
        #Vai para a segunda área
        # myDirection = turnTo(myDirection ,EAST)
        # #MoveDirectionPosition(frente, 0.020)
        # currentPosition += 1
        if(order == 1):
            destine = 55
            direction = LESTE
            lastTurn = -1
            lado ='esquerda'
        if(order == 2):
            destine = 56
            direction = OESTE
            lastTurn = 1
            lado ='direita'

        currentPosition, myDirection = IndoDeA_para_B(adeni,currentPosition, destine, myDirection, SUL)
        alinharLateral(adeni, lado)
        # while Ler_Cor(adeni, 'esquerda')=='BRANCO' and Ler_Cor(adeni , 'direita')== 'BRANCO':
        #     alinharLateral(adeni, lado)
        #     move_frente(adeni, 2)
        #alinhar(adeni, 'frente')
        # print(lado, 'lado')
        andar_em_metros(adeni, lado, velocidade,0.1)
        #alinhar(adeni, 'frente')
        # while Ler_Cor(adeni, 'esquerda')=='BRANCO' and Ler_Cor(adeni , 'direita')== 'BRANCO':
        #     move_frente(adeni, 2)
        giroRSEA(adeni, 1)
        #andar_em_metros(adeni, 'frente', 2,0.08)
        alinhar(adeni , 'frente')
        #alinharComLateralFT(adeni, 'frente', -1)
        andar_em_metros(adeni, 'tras', velocidade,0.08)
        alinhar(adeni, 'tras')
        alinharComLateralFT(adeni, 'tras', 1)
        #alinharComLateralFT(adeni, 'tras', -1)

        andar_em_metros(adeni, 'frente', velocidade,0.035)

        #giroRSEA(adeni)
        #Se posiciona da melhor forma para enxergar os blocos
        #myDirection = corrigindoADirecao(adeni ,myDirection,direction)
        #Align()
        #girar_90_graus(adeni,lastTurn)
        myDirection = NORTE
        #align.Align()
        #alinhar(adeni, 'tras')
        #giroRSEA(adeni)
        matrix1 = visionAlgo.resolveVision(adeni,1) #MODIFICAR MATRIZ

        andar_em_metros(adeni,'frente', velocidade, 0.08)
        andar_em_metros(adeni, lado, velocidade, 0.02) #LINHA NOVA
        matrix1 = invertMatrix(matrix1)
        return matrix1, currentPosition, myDirection

    def getBlocksInformation(currentPosition, myDirection):
        # print(currentPosition)
        # print('get block information')
        if (currentPosition < 40): #Ta na parte de cima
            if(currentPosition % 10 <= 2):
                # print("Primeira área1")
                time.sleep(2)
                matrix0, currentPosition, myDirection = firstAreaCubes(currentPosition, myDirection, 1)
                #Vai para a segunda área
                # print("Segunda área1")

                #MoveDirectionPosition(frente, 0.020)
                # currentPosition += 1
                matrix1, currentPosition, myDirection = secondAreaCubes(currentPosition, myDirection, 2)
            elif(currentPosition % 10 <= 4):
                # print("Primeira área2")
                matrix0, currentPosition, myDirection = firstAreaCubes(currentPosition, myDirection, 1)
                #Vai para a segunda área
                # print("Segunda área2")
                #MoveDirectionPosition(frente, 0.020)
                matrix1, currentPosition, myDirection = secondAreaCubes(currentPosition, myDirection, 2)
            else:
                # print("Primeira área3")
                # print(myDirection)
                matrix1, currentPosition, myDirection = secondAreaCubes(currentPosition, myDirection, 1)
                # print("Segunda área3")
                currentPosition += 1
                matrix0, currentPosition, myDirection = firstAreaCubes(currentPosition, myDirection, 1)
        else: #Ta na parte de baixo
            if(currentPosition % 10 <= 2):
                matrix0, currentPosition, myDirection = thirdAreaCubes(currentPosition, myDirection, 1)
                #Vai para a segunda área
                #myDirection = corrigindoADirecao(adeni,myDirection ,LESTE)
                #MoveDirectionPosition(frente, 0.020)
                # currentPosition += 1
                matrix1, currentPosition, myDirection = fourthAreaCubes(currentPosition, myDirection, 2)
            elif(currentPosition % 10 <= 4):
                matrix0, currentPosition, myDirection = thirdAreaCubes(currentPosition, myDirection, 2)
                #Vai para a segunda área
                #myDirection = corrigindoADirecao(adeni,myDirection ,LESTE)
                #MoveDirectionPosition(frente, 0.020)
                currentPosition-=1
                matrix1, currentPosition, myDirection = fourthAreaCubes(currentPosition, myDirection, 2)
            else:
                matrix1, currentPosition, myDirection = fourthAreaCubes(currentPosition, myDirection, 1)
                #myDirection = corrigindoADirecao(adeni,myDirection ,OESTE)
                # currentPosition -= 1
                matrix0, currentPosition, myDirection = thirdAreaCubes(currentPosition, myDirection, 2)

        #time.sleep(3)

        #myDirection = turnTo(myDirection ,WEST)
        #MoveDirectionPosition(frente, 0.020)
        #currentPosition += 1
        # print(matrix0)
        # print(matrix1)
        matrix = np.concatenate((matrix0, matrix1), axis=0)
        print(matrix)
        #order = gb.get_path(gb.createGraphBlocks(matrix))  #AQUI FUNCIONA COM O CODIGO SIMPLES!!!!!
        # print(order, matrixFinal)
        return currentPosition, myDirection, matrix

    def winOPEN():   
        direc = firstSq.getAngInicial(adeni)
        #print(direc, 'DIREÇÃO VIRADO')
        initialDirection = corrigindoADirecao(adeni,direc,SUL)
        alinhar(adeni, 'frente')
        andar_em_metros(adeni, 'tras', 2, 0.08)
        iniY, iniX = firstSq.identifyFirstPos(adeni)
        initialPosition = [iniY,iniX]
        initialDirection
        # print(initialPosition)
        if(initialPosition[1] == -1):
            moverPorQuadrado(adeni,'frente')
            alinhar(adeni, 'frente')
            andar_em_metros(adeni,'frente', 5, 0.065)
        initialPosition = (iniY+1)*10+(iniX+1)
        # print(initialPosition)
        # time.sleep(50)
        # VERIFICAR ISSO!!!!!!!!!!!!!! PRA PEGAR DIREÇÃO INICIAL
        ##### PARA TESTES ######
        #FIRST AREA:
        #initialPosition = 26
        #SECOND AREA:
        # print('---', matrix, 'DEPOIS DO WIN OPEN')
        # print('---', matrix[0], 'WIN OPEN')
        # print('---', matrix[0][0], 'WIN OPEN')
        # iniY, iniX = firstSq.identifyFirstPos(adeni)
        # initialPosition = [iniY,iniX]
        # initialPosition = (iniY+1)*10+(iniX+1)
        #order = [1, 2, 3]
        pickLater = []
        blockZero = []
        #APENAS TESTE
        #order = gb.get_path(gb.createGraphBlocks(matrix))
        #currentPosition = initialPosition
        #myDirection = initialDirection
        #FIM DE TESTE
        # IndoDeA_para_B(adeni, 26, 22, SUL, SUL)

        currentPosition, myDirection, matrix = getBlocksInformation(initialPosition, initialDirection)
        quantidade_cubos = 0
        while True:
            posicao = [str(currentPosition)[0],str(currentPosition)[1]]

            bloco = melhorbloco(posicao,matrix)
            print('melhor bloco frente: ', bloco)
            local = trajeto(bloco)
            print('local:', local)
            print('posicao atual:', currentPosition)
            currentPosition,minhaDirecao = IndoDeA_para_B(adeni,currentPosition,local,firstSq.getAngInicial(adeni), SUL)

            print('posicao atual2:', currentPosition)

            minhaDirecao = casosEspeciais(adeni,currentPosition,minhaDirecao,bloco)
            quantidade_cubos += alinhar_e_pegar_cubo(adeni,bloco)
            minhaDirecao = firstSq.getAngInicial(adeni)
            minhaDirecao = corrigindoADirecao(adeni, minhaDirecao, SUL)

            if quantidade_cubos == 5:
                adeni.cubo_garra_costas[0] = -1
            print('direção antes de entregar cubo: ', minhaDirecao)
            currentPosition, direcaoFinal = entregandoCubos(adeni,currentPosition,minhaDirecao)


            ###########################################################################

            posicao = [str(currentPosition)[0],str(currentPosition)[1]]

            bloco = melhorbloco(posicao,matrix)
            print('melhor bloco tras: ', bloco)
            local = trajeto(bloco)
            print('local2: ', local)
            currentPosition,minhaDirecao = IndoDeA_para_B(adeni,currentPosition,local,firstSq.getAngInicial(adeni), SUL)

            print('posicao atual3:', currentPosition)

            minhaDirecao = casosEspeciais(adeni,currentPosition,minhaDirecao,bloco)
            quantidade_cubos += alinhar_e_pegar_cubo(adeni,bloco)
            minhaDirecao = firstSq.getAngInicial(adeni)
            minhaDirecao = corrigindoADirecao(adeni, minhaDirecao, SUL)

            currentPosition, direcaoFinal = entregandoCubos(adeni,currentPosition,minhaDirecao)

    winOPEN()
    # while True:
    #     andar_livre(adeni, -1, 6)

else:
    print('Failed connecting to remote API server')
    sys.exit()
