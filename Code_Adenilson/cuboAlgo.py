# coding=utf-8
# Insert in a script in Coppelia

import sim
import globalDefs as glob
from globalDefs import *
import visionAlgo as vis
import locomAlgo as move
import garraAlgo as garra
import sensorAlgo as sense
import alignAlgo as align
import time

### FUNÇÕES CUBOS
def grab(cube):
	#erro, cubo = sim.simxGetObjectHandle(glob.clientID, cube, sim.simx_opmode_blocking)
	erro, pa = sim.simxGetObjectHandle(glob.clientID,'Cuboid_acoplador',sim.simx_opmode_blocking)
	# erro =1
	# while erro != 0:
	#	erro = sim.simxSetObjectIntParameter(glob.clientID, cube, sim.sim_shapeintparam_respondable, 0, sim.simx_opmode_oneshot)
	#	print('respondable', erro)
	# time.sleep(1)
	# erro = 1
	# while erro != 0:
	#	erro = sim.simxSetObjectIntParameter(glob.clientID, cube, sim.sim_shapeintparam_static, 1, sim.simx_opmode_oneshot)
	#	print('dynamic', erro)
	# time.sleep(1)
	#print(sim.simxSetModelProperty(glob.clientID, cubo, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot))
	#time.sleep(1)
	erro = 1
	while erro != 0:
		erro = sim.simxSetObjectParent(glob.clientID, cube, pa, True, sim.simx_opmode_oneshot)
		#print('parent', erro)
	time.sleep(3)


def leave(cube):
	#erro, cubo = sim.simxGetObjectHandle(glob.clientID, cube, sim.simx_opmode_blocking)
	erro, pa = sim.simxGetObjectHandle(glob.clientID,'Cuboid_acoplador',sim.simx_opmode_blocking)
	sim.simxSetObjectParent(glob.clientID, cube, -1, True, sim.simx_opmode_oneshot_wait)
	erro =1
	while erro != 0:
		erro = sim.simxSetObjectIntParameter(glob.clientID, cube, sim.sim_shapeintparam_respondable, 1, sim.simx_opmode_oneshot)
		#print('respondable', erro)
	time.sleep(0.1)
	erro = 1
	while erro != 0:
	   erro = sim.simxSetObjectIntParameter(glob.clientID, cube, sim.sim_shapeintparam_static, 0, sim.simx_opmode_oneshot)
	   #print('dynamic', erro)
	#print(sim.simxSetModelProperty(glob.clientID, cubo, sim.sim_modelproperty_not_dynamic, sim.simx_opmode_oneshot))
	time.sleep(0.1)

	## FUNÇÕES PEGAR CUBO ########################################

def empurrar_cubo():
	move.MoveDirectionPosition(tras, 0.12)
	garra.fechar_garra_total()
	while(sense.getDistanceIR(glob.irLeft) > 0.01 or sense.getDistanceIR(glob.irRight) > 0.01):
		move.MoveForward(2)
	move.Stop()
	move.MoveDirectionPosition(frente, 0.04)

def pegar_cubo():
	garra.abrir_garra()
	garra.descer_elevador()
	garra.fechar_garra()
	garra.subir_elevador(SEGUNDO_ANDAR)

def identificar_valor(blockColor):

	if (blockColor == 'W'):
		text, op2 = vis.getNumber(glob.clientID)
		print(text,op2)
		if(op2[0] == -1):
			return -1

		if(int(text) == op2[0]):
			return int(text)
		elif(op2[1] < 0.1):
			text_, op2_ = vis.getNumber(glob.clientID)
			if(op2[0] == -1):
				return -1
			if(int(text_) == op2_[0]):
				return int(text_)
			elif(op2_[1] < 0.1):
				return int(op2_[0])
		return int(text)
	if(blockColor == 'K'):
		num1 = vis.getCode(glob.clientID)
		num2 = vis.getCode(glob.clientID)
		if(num1 == num2):
			return num1
		else:
			return identificar_valor(blockColor)
	return 16

def chegar_perto_prateleira():
	a = sense.getDistanceIR(glob.irLeft)
	b = sense.getDistanceIR(glob.irRight)
	#print('chegando')
	move.MoveForward(3)
	while(a > 0.07 or b > 0.07):
		#print(sense.getDistanceIR(glob.irLeft), sense.getDistanceIR(glob.irRight))
		a = sense.getDistanceIR(glob.irLeft)
		b = sense.getDistanceIR(glob.irRight)
	move.Stop()

def entregar_cubo_colorido(cube):

    align.Align()
    garra.descer_elevador()
    leave(cube)
    garra.abrir_garra()
    #empurrar_cubo()
    garra.subir_elevador(SEGUNDO_ANDAR)
    garra.fechar_garra_total()
    move.MoveDirectionPosition(tras, 0.05)

def entregar_cubo_terceiro_andar(cube):
	garra.subir_elevador(TERCEIRO_ANDAR)
	move.MoveDirectionPosition(frente, 0.1)
	chegar_perto_prateleira()
	garra.abrir_garra()
	leave(cube)
	#empurrar_cubo()
	#print("Vou dar ré")
	align.AlignBack(3)
	garra.fechar_garra_total()
	garra.subir_elevador(SEGUNDO_ANDAR)

def entregar_cubo_segundo_andar(cube):
	#print('vou entregar')
	garra.subir_elevador(SEGUNDO_ANDAR)
	move.MoveDirectionPosition(frente, 0.1)
	chegar_perto_prateleira()
	leave(cube)
	garra.abrir_garra()
	#empurrar_cubo()
	align.AlignBack(3)
	garra.fechar_garra_total()
	garra.subir_elevador(SEGUNDO_ANDAR)

def entregar_cubo_primeiro_andar(cube):
	garra.subir_elevador(PRIMEIRO_ANDAR)
	move.MoveDirectionPosition(frente, 0.1)
	chegar_perto_prateleira()
	leave(cube)
	garra.abrir_garra()
	#empurrar_cubo()
	align.AlignBack(3)
	garra.fechar_garra_total()
	garra.subir_elevador(SEGUNDO_ANDAR)

def alinhar_cubo_na_esquerda_e_pegar():

	move.andar_em_metros(tras, 2, 0.01)
	garra.fechar_garra_total()
	garra.descer_elevador()
	while True :
		a = sense.getDistanceIR(glob.irRight)
		b = sense.getDistanceIR(glob.irLeft)
		#print(a,b)
		move.MoveForward(2)
		if(b<0.03 or a < 0.03):
			break
	move.Stop()
	a = sense.getDistanceIR(glob.irRight)
	b = sense.getDistanceIR(glob.irLeft)
	if(b < a):
		cube = sense.getCubeHandle(glob.irLeft)
		dist = b
	else:
		cube = sense.getCubeHandle(glob.irRight)
		dist = a
	garra.abrir_garra()
	esq=0
	# while True :
	#	 a = sense.getDistanceIR(glob.irRight)
	#	 b = sense.getDistanceIR(glob.irLeft)
		# print(a,b)
		# giro_livre(direita, 2)
		# # if(b<1): 
		# #	 esq=esq+1
	#	 # if(a<1 and esq>0):
	#	 #	 break
	#	 if(b<0.015):
	#		 break
	
	#TurnDirectionAng(esquerda, 5)
	# move.Stop()
	# TurnRight()
	# time.sleep(0.08)
	# move.Stop()
	print(dist)
	move.andar_em_metros(frente, 2, dist+0.01)
	garra.fechar_garra_cubo(cube)
	grab(cube)
	garra.subir_elevador(SEGUNDO_ANDAR)
	#align.AlignSpecial(2)
	#move.MoveDirectionPosition(tras, dist)
	return cube

def alinhar_cubo_na_direita_e_pegar():
	move.andar_em_metros(tras, 2, 0.01)
	garra.fechar_garra_total()
	garra.descer_elevador()
	while True :
		a = sense.getDistanceIR(glob.irRight)
		b = sense.getDistanceIR(glob.irLeft)
		#print(a,b)
		
		if(b<0.03 or a < 0.03):
			break
		move.MoveForward(2)
	move.Stop()
	a = sense.getDistanceIR(glob.irRight)
	b = sense.getDistanceIR(glob.irLeft)
	if(b < a):
		cube = sense.getCubeHandle(glob.irLeft)
		dist = b
	else:
		cube = sense.getCubeHandle(glob.irRight)
		dist = a
	garra.abrir_garra()

	dirt=0
	# while True :
	#	 a = sense.getDistanceIR(glob.irRight)
	#	 b = sense.getDistanceIR(glob.irLeft)
	#	 print(a,b)
	#	 giro_livre(esquerda, 2)
	#	 # if(a<1): 
	#	 #	 dirt=dirt+1
	#	 # if(b<1 and dirt>0):
	#	 #	 break
	#	 if(a < 0.15):
	#		 break
	move.Stop()

	#TurnDirectionAng(direita, 5)
	# move.Stop()
	# TurnLeft()
	# time.sleep(0.08)
	# move.Stop()
	move.andar_em_metros(frente, 2, dist+0.01)

	garra.fechar_garra_cubo(cube)
	grab(cube)
	print('vou subir')
	garra.subir_elevador(SEGUNDO_ANDAR)
	print('subi')
	#align.AlignSpecial(2)
	#time.sleep(2)
	#move.MoveDirectionPosition(tras, dist)
	return cube
