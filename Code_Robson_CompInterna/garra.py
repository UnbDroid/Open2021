import sim
import numpy as np
import time
import simConst

## FUNÇÕES DA GARRA ######################################

#Nas funções da garra, vamos ter que definir quando quisermos manipular uma das duas garras, pois como agora vamos ter duas, isso vai ter que ser especificado em cada função de mover a garra

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
    sim.simxSetJointTargetPosition(object.clientID,object.pa_direita1,-1*position,sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)

def fechar_garra_costas(object, position):
    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetPosition(object.clientID,object.pa_esquerda2,position,sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(object.clientID,object.pa_direita2,-1*position,sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)


def abrir_garra_frente(object, position):
    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetPosition(object.clientID,object.pa_esquerda1,-1*position,sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(object.clientID,object.pa_direita1,position,sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)

def abrir_garra_costas(object, position):
    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetPosition(object.clientID,object.pa_esquerda2,-1*position,sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(object.clientID,object.pa_direita2,position,sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)

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
    # while erro != 0:
    #     erro, robotPosition = sim.simxGetObjectPosition(object.clientID, object.robot, -1, sim.simx_opmode_streaming)
    # erro = 1
    while erro != 0:
        erro, cubePosition = sim.simxGetObjectPosition(object.clientID, cube, object.robot, sim.simx_opmode_streaming)
    #print(robotPosition)
    # print('Antes: ', cubePosition)
    cubePosition[0] = -0.02
    cubePosition[1] = 0.02
    cubePosition[2] = 0.03
    # print('Depois: ', cubePosition)

    erro = 1
    while erro != 0: #verificar se essa parte ta certa
        sim.simxPauseCommunication(object.clientID, True)
        sim.simxSetJointTargetPosition(object.clientID,object.paDireita1,0.02,sim.simx_opmode_oneshot) 
        sim.simxSetJointTargetPosition(object.clientID,object.paEsquerda1,-0.02,sim.simx_opmode_oneshot)
        erro = sim.simxSetObjectPosition(object.clientID, cube, object.garraEsq, cubePosition, sim.simx_opmode_oneshot)
        sim.simxSetObjectParent(object.clientID, cube, object.garraEsq, True, sim.simx_opmode_oneshot)
        sim.simxSetObjectIntParameter(object.clientID, cube, 3003, 1, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(object.clientID, False)
    time.sleep(1)

def abrir_garra_frente_cubo(object, cube):
    # erro = 1
    # while erro != 0:
    #     erro, cubePosition = sim.simxGetObjectPosition(object.clientID, cube, -1, sim.simx_opmode_streaming)
    # # cubePosition[2] = 0
    # erro = 1
    # while erro != 0: #verificar se essa parte ta certa
    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetPosition(object.clientID, object.paDireita1, 0, sim.simx_opmode_oneshot) #ver essas distâncias pra deixar a garra aberta
    sim.simxSetJointTargetPosition(object.clientID, object.paEsquerda1, 0, sim.simx_opmode_oneshot) #ver essas distâncias pra deixar a garra aberta
    # erro = sim.simxSetObjectPosition(object.clientID, cube, object.robot, cubePosition, sim.simx_opmode_oneshot)#talvez de pra tirar essa linha e tirar o while
    sim.simxSetObjectParent(object.clientID, cube, -1, True, sim.simx_opmode_oneshot)
    sim.simxSetObjectIntParameter(object.clientID, cube, 3003, 0, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)
        #erro = 0
    time.sleep(1)

def fechar_garra_costas_cubo(object, cube):
    erro = 1
    # while erro != 0:
    #     erro, robotPosition = sim.simxGetObjectPosition(object.clientID, object.robot, -1, sim.simx_opmode_streaming)
    # erro = 1
    while erro != 0:
        erro, cubePosition = sim.simxGetObjectPosition(object.clientID, cube, object.robot, sim.simx_opmode_streaming)
    #print(robotPosition)
    # print('Antes: ', cubePosition)
    cubePosition[0] = -0.02
    cubePosition[1] = 0.02
    cubePosition[2] = 0.03
    # print('Depois: ', cubePosition)

    erro = 1
    while erro != 0: #verificar se essa parte ta certa
        sim.simxPauseCommunication(object.clientID, True)
        sim.simxSetJointTargetPosition(object.clientID,object.paDireita2,0.02,sim.simx_opmode_oneshot) 
        sim.simxSetJointTargetPosition(object.clientID,object.paEsquerda2,-0.02,sim.simx_opmode_oneshot)
        erro = sim.simxSetObjectPosition(object.clientID, cube, object.garraEsq, cubePosition, sim.simx_opmode_oneshot)
        sim.simxSetObjectParent(object.clientID, cube, object.garraEsq, True, sim.simx_opmode_oneshot)
        sim.simxSetObjectIntParameter(object.clientID, cube, 3003, 1, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(object.clientID, False)
    time.sleep(1)

def abrir_garra_costas_cubo(object, cube):
    # erro = 1
    # while erro != 0:
    #     erro, cubePosition = sim.simxGetObjectPosition(object.clientID, cube, -1, sim.simx_opmode_streaming)
    # # cubePosition[2] = 0
    # erro = 1
    # while erro != 0: #verificar se essa parte ta certa
    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetPosition(object.clientID, object.paDireita2, 0, sim.simx_opmode_oneshot) #ver essas distâncias pra deixar a garra aberta
    sim.simxSetJointTargetPosition(object.clientID, object.paEsquerda2, 0, sim.simx_opmode_oneshot) #ver essas distâncias pra deixar a garra aberta
    # erro = sim.simxSetObjectPosition(object.clientID, cube, object.robot, cubePosition, sim.simx_opmode_oneshot)#talvez de pra tirar essa linha e tirar o while
    sim.simxSetObjectParent(object.clientID, cube, -1, True, sim.simx_opmode_oneshot)
    sim.simxSetObjectIntParameter(object.clientID, cube, 3003, 0, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)
        #erro = 0
    time.sleep(1)
