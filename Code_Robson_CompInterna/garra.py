import sim
import numpy as np
import time
import simConst

## FUNÇÕES DA GARRA ######################################


#essas funções de subir e descer a garra estavam sem a parte de pauseCommunication, não sei se tem problema
def subir_garra_frente(object, altura):
    sim.simxSetJointTargetPosition(object.clientID,object.acoplador_garra1,altura,sim.simx_opmode_oneshot) 
    time.sleep(1)

def subir_garra_costas(object, altura):
    sim.simxSetJointTargetPosition(object.clientID,object.acoplador_garra2,altura,sim.simx_opmode_oneshot) 
    time.sleep(1)

def descer_garra_frente(object):
    sim.simxSetJointTargetPosition(object.clientID,object.acoplador_garra1,-0.15,sim.simx_opmode_oneshot)
    time.sleep(1)

def descer_garra_costas(object):
    sim.simxSetJointTargetPosition(object.clientID,object.acoplador_garra2,-0.15,sim.simx_opmode_oneshot)
    time.sleep(1)

def fechar_garra_frente(object, position):
    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetPosition(object.clientID,object.pa_esquerda1,position,sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(object.clientID,object.pa_direita1,position,sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)
    time.sleep(1)

def fechar_garra_costas(object, position):
    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetPosition(object.clientID,object.pa_esquerda2,position,sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(object.clientID,object.pa_direita2,position,sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)
    time.sleep(1)


def abrir_garra_frente(object, position):
    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetPosition(object.clientID,object.pa_esquerda1,position,sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(object.clientID,object.pa_direita1,position,sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)
    time.sleep(1)

def abrir_garra_costas(object, position):
    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetPosition(object.clientID,object.pa_esquerda2,position,sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(object.clientID,object.pa_direita2,position,sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)
    time.sleep(1)

def enable_magic_cube(object, cubo):
	sim.simxPauseCommunication(object.clientID, True)
	sim.simxSetModelProperty(object.clientID, cubo, simConst.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
	sim.simxSetObjectParent(object.clientID, cubo, object.robot, True, sim.simx_opmode_oneshot)
	sim.simxPauseCommunication(object.clientID, False)


def disable_magic_cube(object, cubo):
	sim.simxPauseCommunication(object.clientID, True)
	sim.simxSetObjectParent(object.clientID, cubo, -1, True, sim.simx_opmode_oneshot)
	sim.simxSetModelProperty(object.clientID, cubo, not simConst.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
	sim.simxPauseCommunication(object.clientID, False)


def fechar_garra_frente_cubo(object, cube):
    erro = 1
    while erro != 0:
        erro, cubePosition = sim.simxGetObjectPosition(object.clientID, cube, object.robot, sim.simx_opmode_streaming)
    cubePosition[0] = 0.04 #se aumentar, vai mais para baixo
    cubePosition[1] = 0 #se aumentar, vai mais para dentro do robô
    cubePosition[2] = 0 #se aumentar, vai mais para a esquerda

    erro = 1
    while erro != 0:
        sim.simxPauseCommunication(object.clientID, True)
        sim.simxSetObjectIntParameter(object.clientID, cube, 3003, 1, sim.simx_opmode_oneshot)# torna o cubo estático
        # sim.simxSetJointTargetPosition(object.clientID,object.pa_direita1,0.2,sim.simx_opmode_oneshot) #se pa não precisa fechar a garra
        # sim.simxSetJointTargetPosition(object.clientID,object.pa_esquerda1,0.2,sim.simx_opmode_oneshot)
        erro = sim.simxSetObjectPosition(object.clientID, cube, object.pa_esquerda1, cubePosition, sim.simx_opmode_oneshot)
        sim.simxSetObjectParent(object.clientID, cube, object.cubo_acoplador1, True, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(object.clientID, False)
    time.sleep(1)

def abrir_garra_frente_cubo(object, cube):
    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetPosition(object.clientID, object.pa_direita1, 0.005, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(object.clientID, object.pa_esquerda1, 0.005, sim.simx_opmode_oneshot)
    sim.simxSetObjectParent(object.clientID, cube, -1, True, sim.simx_opmode_oneshot)
    sim.simxSetObjectIntParameter(object.clientID, cube, 3004, 1, sim.simx_opmode_oneshot) # torna o cubo respondable
    sim.simxSetObjectIntParameter(object.clientID, cube, 3003, 0, sim.simx_opmode_oneshot) # torna o cubo dinâmico
    sim.simxPauseCommunication(object.clientID, False)
    time.sleep(1)

def fechar_garra_costas_cubo(object, cube):
    erro = 1
    while erro != 0:
        erro, cubePosition = sim.simxGetObjectPosition(object.clientID, cube, object.robot, sim.simx_opmode_streaming)
    cubePosition[0] = 0.04 #se aumentar, vai mais para baixo
    cubePosition[1] = 0 #se aumentar, vai mais para dentro do robô
    cubePosition[2] = 0 #se aumentar, vai mais para a esquerda

    erro = 1
    while erro != 0:
        sim.simxPauseCommunication(object.clientID, True)
        sim.simxSetObjectIntParameter(object.clientID, cube, 3003, 1, sim.simx_opmode_oneshot)# torna o cubo estático
        # sim.simxSetJointTargetPosition(object.clientID,object.pa_direita2,0.2,sim.simx_opmode_oneshot) #se pa não precisa fechar a garra
        # sim.simxSetJointTargetPosition(object.clientID,object.pa_esquerda2,0.2,sim.simx_opmode_oneshot)
        erro = sim.simxSetObjectPosition(object.clientID, cube, object.pa_esquerda2, cubePosition, sim.simx_opmode_oneshot)
        sim.simxSetObjectParent(object.clientID, cube, object.cubo_acoplador2, True, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(object.clientID, False)
    time.sleep(1)

def abrir_garra_costas_cubo(object, cube):
    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetPosition(object.clientID, object.pa_direita2, 0.005, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(object.clientID, object.pa_esquerda2, 0.005, sim.simx_opmode_oneshot)
    sim.simxSetObjectParent(object.clientID, cube, -1, True, sim.simx_opmode_oneshot)
    sim.simxSetObjectIntParameter(object.clientID, cube, 3004, 1, sim.simx_opmode_oneshot) # torna o cubo respondable
    sim.simxSetObjectIntParameter(object.clientID, cube, 3003, 0, sim.simx_opmode_oneshot) # torna o cubo dinâmico
    sim.simxPauseCommunication(object.clientID, False)
    time.sleep(1)