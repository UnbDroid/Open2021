import sim
import numpy as np
import time
import simConst
from motor import stop

## FUNÇÕES DE GIRAR ######################################


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