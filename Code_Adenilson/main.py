import time
import sys

from garra import *
from girar import *
from motor import *
from sensor import *
from object_handle import ObjectHandle
from andarPorQuadrado import *
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
    IndoDeA_para_B(adeni,31,34,SUL,SUL)
    # IndoDeA_para_B(adeni,64,61,SUL,SUL)
    # IndoDeA_para_B(adeni,61,21,SUL,SUL)
    # IndoDeA_para_B(adeni,21,27,SUL,LESTE)
    
    


else:
    print('Failed connecting to remote API server')
    sys.exit()
