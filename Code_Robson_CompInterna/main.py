import time
import sys

from garra import *
from girar import *
from motor import *
from sensor import *
from object_handle import ObjectHandle
import visionAlgo

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
    girando = 0
    cor_esquerda = Ler_Cor(adeni ,'esquerda')
    cor_direita = Ler_Cor(adeni, 'direita')

    def alinhar():
        while True:
            esquerda = Ler_Cor(adeni, 'esquerda')
            direita = Ler_Cor(adeni, 'direita')
            if esquerda =='PRETO' or direita =='preto':
                print('quebrei')
                break
            else:
                print('to andando')
                move_frente(adeni,3)
        while True:
            flag = 0
            corE =Ler_Cor(adeni, 'esquerda')
            corD = Ler_Cor(adeni, 'direita')
            if flag:
                break
            while Ler_Cor(adeni, 'esquerda')== 'PRETO' and Ler_Cor(adeni, 'direita') == 'BRANCO':
                print('cor esquerda PRETO')
                giro_livre(adeni, 1,1)
                flag =1
            while Ler_Cor(adeni, 'esquerda') == 'BRANCO' and Ler_Cor(adeni, 'direita') == 'PRETO':
                print('cor direita PRETA')
                giro_livre(adeni, -1,1)
                flag = 1
            else:
                move_frente(adeni, 3)
    #while True:
     #   alinhar()
        
    # while True:
    # turn_around_angle(adeni, 100, 1, 2)
    # girar_90_graus(adeni, 1)

    # girar_90_graus(adeni, 1)

    # giro_livre(adeni,1,2)
    # andar_em_metros(adeni, 'tras', 2, 1)
    #while girando<1:
     #   alinhar
    


else:
    print('Failed connecting to remote API server')
    sys.exit()
