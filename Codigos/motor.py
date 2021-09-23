import sim
import numpy as np
import time
import simConst

## FUNÇÕES DE LOCOMOÇAO ######################################


def stop(object):
	sim.simxPauseCommunication(object.clientID, True)
	sim.simxSetJointTargetVelocity(object.clientID, object.omniWheel_direita_frente, 0, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID, object.omniWheel_direita_atras, 0, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID, object.omniWheel_esquerda_frente, 0, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID, object.omniWheel_esquerda_atras, 0, sim.simx_opmode_oneshot)
	sim.simxPauseCommunication(object.clientID, False)
	time.sleep(0.1)


def move_forward(object,v):
	sim.simxPauseCommunication(object.clientID, True)
	sim.simxSetJointTargetVelocity(object.clientID,object.omniWheel_direita_frente, -v, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID,object.omniWheel_direita_atras, -v, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID,object.omniWheel_esquerda_frente, -v, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID,object.omniWheel_esquerda_atras, -v, sim.simx_opmode_oneshot)
	sim.simxPauseCommunication(object.clientID, False)


def move_tras(object,v):
	sim.simxPauseCommunication(object.clientID, True)
	sim.simxSetJointTargetVelocity(object.clientID,object.omniWheel_direita_frente, -v, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID,object.omniWheel_direita_atras, -v, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID,object.omniWheel_esquerda_frente, v, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID,object.omniWheel_esquerda_atras, v, sim.simx_opmode_oneshot)
	sim.simxPauseCommunication(object.clientID, False)


def move_frente(object,v):
	sim.simxPauseCommunication(object.clientID, True)
	sim.simxSetJointTargetVelocity(object.clientID,object.omniWheel_direita_frente, v, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID,object.omniWheel_direita_atras, v, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID,object.omniWheel_esquerda_frente, -v, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID,object.omniWheel_esquerda_atras, -v, sim.simx_opmode_oneshot)
	sim.simxPauseCommunication(object.clientID, False)

def andar_livre(object,d,v):

	# d = 1 , esquerda
	# d =-1 , direita
	# v = velocidade

	sim.simxPauseCommunication(object.clientID, True)
	sim.simxSetJointTargetVelocity(object.clientID, object.omniWheel_direita_frente, -v*d, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID, object.omniWheel_esquerda_frente, -v*d, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID, object.omniWheel_direita_atras, +v*d, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(object.clientID, object.omniWheel_esquerda_atras, +v*d, sim.simx_opmode_oneshot)
	sim.simxPauseCommunication(object.clientID, False)

def andar_em_metros(object, d, v, m):
	# d = 8 , andar para frente
	# d = 2 , andar para trás
	# d = 4 , andar para esquerda
	# d = 6 , andar para direita
	# v = velocidade
	# m = valor em metros

	erro,a_inicial=sim.simxGetObjectPosition(object.clientID,object.robot,-1,sim.simx_opmode_blocking)
	x_inicial=a_inicial[0]
	y_inicial=a_inicial[1]

	if d == 8:
		move_frente(object, v)
	if d == 2:
		move_tras(object, v)
	if d == 4:
		andar_livre(object, -1, v)
	if d == 6:
		andar_livre(object, 1, v)

	while True:
		erro,a=sim.simxGetObjectPosition(object.clientID,object.robot,-1,sim.simx_opmode_blocking)
		x=a[0]
		y=a[1]
		# print(x,y)
		if(abs(x-x_inicial)>=m or abs(y-y_inicial)>=m):
			# print("PAAAAAAAAAAARARARARAR")
			stop(object)
			break
	stop(object)
