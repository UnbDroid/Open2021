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
