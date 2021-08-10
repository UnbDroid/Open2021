import sim
import numpy as np
import time
import simConst

## FUNÇÕES DA GARRA ######################################

#Nas funções da garra, vamos ter que definir quando quisermos manipular uma das duas garras, pois como agora vamos ter duas, isso vai ter que ser especificado em cada função de mover a garra
def close_arms(object, position):
    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetPosition(object.clientID,object.leftArmFrente,position,sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(object.clientID,object.rightArmFrente,-1*position,sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)


def open_arms(object, position):
    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetPosition(object.clientID,object.leftArmFrente,-1*position,sim.simx_opmode_oneshot)
    sim.simxSetJointTargetPosition(object.clientID,object.rightArmFrente,position,sim.simx_opmode_oneshot)
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