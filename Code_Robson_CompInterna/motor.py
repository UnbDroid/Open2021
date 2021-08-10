import sim
import numpy as np
import time
import simConst

## FUNÇÕES DE LOCOMOÇAO ######################################


def stop(object):
	sim.simxPauseCommunication(object.clientID, True)
	sim.simxSetJointTargetVelocity(object.clientID,object.robotFrontRightMotor, 0, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID,object.robotFrontLeftMotor, 0, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID,object.robotBackRightMotor, 0, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID,object.robotBackLeftMotor, 0, sim.simx_opmode_oneshot)
	sim.simxPauseCommunication(object.clientID, False)


def move_forward(object,v):
	sim.simxPauseCommunication(object.clientID, True)
	sim.simxSetJointTargetVelocity(object.clientID,object.robotFrontRightMotor, -v, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID,object.robotBackRightMotor, -v, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID,object.robotFrontLeftMotor, -v, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID,object.robotBackLeftMotor, -v, sim.simx_opmode_oneshot)
	sim.simxPauseCommunication(object.clientID, False)


def move_back(object,v):
	sim.simxPauseCommunication(object.clientID, True)
	sim.simxSetJointTargetVelocity(object.clientID,object.robotFrontRightMotor, v, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID,object.robotBackRightMotor, v, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID,object.robotFrontLeftMotor, v, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID,object.robotBackLeftMotor, v, sim.simx_opmode_oneshot)
	sim.simxPauseCommunication(object.clientID, False)


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

def able_magic_cube(object, cubo):
	sim.simxPauseCommunication(object.clientID, True)
	sim.simxSetModelProperty(object.clientID, cubo, simConst.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
	sim.simxSetObjectParent(object.clientID, cubo, object.robot, True, sim.simx_opmode_oneshot)
	sim.simxPauseCommunication(object.clientID, False)


def disable_magic_cube(object, cubo):
	sim.simxPauseCommunication(object.clientID, True)
	sim.simxSetObjectParent(object.clientID, cubo, -1, True, sim.simx_opmode_oneshot)
	sim.simxSetModelProperty(object.clientID, cubo, not simConst.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot)
	sim.simxPauseCommunication(object.clientID, False)

def giro_livre(object, d, v):

    # d = 1 , anti horario, esquerda
    # d =-1 , horario, direita
    # v = velocidade
    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetVelocity(object.clientID,object.robotFrontRightMotor,(-1)*d*v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(object.clientID,object.robotFrontLeftMotor,d*v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(object.clientID,object.robotBackRightMotor,(-1)*d*v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(object.clientID,object.robotBackLeftMotor,d*v, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)


def get_angle_that_makes_sense(object):
	erro,euler_angles=sim.simxGetObjectOrientation(object.clientID,object.bloco_frente,-1,sim.simx_opmode_streaming)
	while(erro !=0):
		erro,euler_angles=sim.simxGetObjectOrientation(object.clientID,object.bloco_frente,-1,sim.simx_opmode_streaming)

	# print(erro, euler_angles)
	factor = 90
	# print(factor)
	if(euler_angles[0] <= 0): factor = 270
	# print(factor)
	# print((np.sign(euler_angles[0]) * 60*euler_angles[1]))
	finalAngle = (np.sign(euler_angles[0]) * 60*euler_angles[1]) + factor
	return finalAngle


def turn_around_angle(object, angle, sentido, velocidade):
	#sentido = 1 roda em sentido antihorario
	#sentido = -1 roda em sentido horario
	current_angle = get_angle_that_makes_sense(object)
	# print(angle)
	if angle < 0:
		angle = angle + 360
	elif angle > 360:
		angle = angle - 360
	# print(angle)
	# print(current_angle)
	if angle == 270:
		angle = 269
	while angle != int(current_angle):
		# print(int(current_angle))

		giro_livre(object, sentido, velocidade)

		current_angle = get_angle_that_makes_sense(object)
	stop(object)

def andar_em_metros(object,d,v,m):
	# d = 1 , andar para frente
	# d =-1 , andar para trás
	# v = velocidade
	# m = valor em metros
	d = d*-1


	erro,a_inicial=sim.simxGetObjectPosition(object.clientID,object.robot,-1,sim.simx_opmode_blocking)
	x_inicial=a_inicial[0]
	y_inicial=a_inicial[1]
	sim.simxPauseCommunication(object.clientID, True)
	sim.simxSetJointTargetVelocity(object.clientID, object.robotFrontRightMotor,d*v, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID, object.robotFrontLeftMotor,d*v, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID, object.robotBackRightMotor,d*v, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID, object.robotBackLeftMotor,d*v, sim.simx_opmode_oneshot)
	sim.simxPauseCommunication(object.clientID, False)
	while(True):
		erro,a=sim.simxGetObjectPosition(object.clientID,object.robot,-1,sim.simx_opmode_blocking)
		x=a[0]
		y=a[1]
		#print(x,y)
		if(abs(x-x_inicial)>=m or abs(y-y_inicial)>=m):
			break
	stop(object)
