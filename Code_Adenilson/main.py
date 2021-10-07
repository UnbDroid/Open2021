import time
import sys

from garra import *
from girar import *
from motor import *
from sensor import *
from logLocomAlgo import *
from object_handle import ObjectHandle
from andarPorQuadrado import *
from visionAlgo import *
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


def firstAreaCubes(currentPosition, myDirection, order):
    if(order == 1):
        destine = 22
        direction = LESTE
        lastTurn = direita
    if(order == 2):
        destine = 23
        direction = OESTE
        lastTurn = esquerda
    #Vai para a primeira área
    currentPosition, myDirection = deA_para_B(adeni, currentPosition, destine, myDirection)
    #Se posiciona da melhor forma para enxergar os blocos
    myDirection = turnTo(adeni, myDirection ,direction, True)
    #Align() #TurnTo ja alinha
    andar_em_metros(adeni,frente, 2, 0.04)
    girar_90_graus(adeni,lastTurn)
    myDirection = SUL
    #align.Align()
    andar_em_metros(adeni, tras, 5, 0.065)
    matrix0 = vis.resolveVision(adeni, 0)
    #time.sleep(3)
    return matrix0, currentPosition, myDirection


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
    initialDirection = SUL
    print(sim.simxGetObjectHandle(clientID, 'Camera_Superior_Vision', sim.simx_opmode_blocking))
    initialPosition = firstSq.identifyFirstPos(adeni)
    if(initialPosition[1] == -1):
        andar_em_metros(frente, 6, 0.20)
        # align.Align()
        move.andar_em_metros(tras, 5, 0.065)
    iniY, iniX = firstSq.identifyFirstPos(adeni)
    initialPosition = (iniY+1)*10+(iniX+1)
    firstAreaCubes(initialPosition, initialDirection, 1) #vai quebrar não está pronto
    # IndoDeA_para_B(adeni,31,34,SUL,SUL)
    # IndoDeA_para_B(adeni,64,61,SUL,SUL)
    # IndoDeA_para_B(adeni,61,21,SUL,SUL)
    # IndoDeA_para_B(adeni,21,27,SUL,LESTE)




else:
    print('Failed connecting to remote API server')
    sys.exit()
