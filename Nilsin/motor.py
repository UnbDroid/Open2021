import sim
import numpy as np
import time
import simConst
from girar import *
from sensor import *


## FUNÇÕES DE LOCOMOÇAO ######################################


def teste(object):
    girar_90_graus(object, 1)


def stop(object):
    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_direita_frente, 0, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_direita_atras, 0, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_esquerda_frente, 0, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_esquerda_atras, 0, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)
    time.sleep(0.1)


def move_forward(object, v):
    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_direita_frente, -v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_direita_atras, -v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_esquerda_frente, -v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_esquerda_atras, -v, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)


def move_tras(object, v):
    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_direita_frente, -v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_direita_atras, -v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_esquerda_frente, v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_esquerda_atras, v, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)


def move_frente(object, v):
    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_direita_frente, v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_direita_atras, v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_esquerda_frente, -v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_esquerda_atras, -v, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)


def andar_livre(object, d, v):

    # d = 1 , esquerda
    # d =-1 , direita
    # v = velocidade

    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_direita_frente, -v*d, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_esquerda_frente, -v*d, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_direita_atras, +v*d, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_esquerda_atras, +v*d, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)


def andar_em_metros(object, d, v, m):
    # d = 8 , andar para frente
    # d = 2 , andar para trás
    # d = 4 , andar para esquerda
    # d = 6 , andar para direita
    # v = velocidade
    # m = valor em metros

    erro, a_inicial = sim.simxGetObjectPosition(
        object.clientID, object.robot, -1, sim.simx_opmode_blocking)
    x_inicial = a_inicial[0]
    y_inicial = a_inicial[1]

    if d == 8:
        move_frente(object, v)
    if d == 2:
        move_tras(object, v)
    if d == 4:
        andar_livre(object, -1, v)
    if d == 6:
        andar_livre(object, 1, v)

    while True:
        erro, a = sim.simxGetObjectPosition(
            object.clientID, object.robot, -1, sim.simx_opmode_blocking)
        x = a[0]
        y = a[1]
        # print(x,y)
        if(abs(x-x_inicial) >= m or abs(y-y_inicial) >= m):
            # print("PAAAAAAAAAAARARARARAR")
            stop(object)
            break
    stop(object)


def alinhar(object):
    while True:
        esquerda = Ler_Cor(object, 'esquerda')
        direita = Ler_Cor(object, 'direita')
        if esquerda == 'PRETO' or direita == 'PRETO':
            print('quebrei')
            stop(object)
            break

        else:
            # print('to andando')
            move_frente(object, 3)
    flag = 0
    while True:
        
        corE = Ler_Cor(object, 'esquerda')
        print("COR ESQUERDA == ", corE)
        corD = Ler_Cor(object, 'direita')
        print("COR DIREITA == ", corD)

        if flag:
            break
        if corE == 'PRETO' and corD == 'PRETO':
            break
        while Ler_Cor(object, 'esquerda') == 'PRETO' and Ler_Cor(object, 'direita') == 'BRANCO':
            # print('cor esquerda PRETO')
            giro_livre(object, -1, 1)
            flag = 1
        while Ler_Cor(object, 'esquerda') == 'BRANCO' and Ler_Cor(object, 'direita') == 'PRETO':
            print('cor direita PRETA')
            giro_livre(object, 1, 1)
            flag = 1
        # else:
        move_frente(object, 3)
    stop(object)        

# Girar para a direita ou para a esquerda pelo angulo que você escolher


def direcaoEGiro(object, ang):
    if (ang == 180):
        print("EAE BRIWBS")
        # pass
        #turn_around_angle(object, 180, -1, 3.60)
        girar_90_graus(object, 1)
        # girar_90_graus(object, -1)
        print("EAE 222222")

    else:
        print("EAE BASDASDASDAS")
        # pass
        girar_90_graus(object, 1)

def MoveForwardPosition(object, dist):
    MoveDirectionPosition(object, 8, dist)

def moverParaFrentePorQuadrado(object, d):
    andar_em_metros(object, d, 6, 0.20)
    alinhar(object)

def andarParaOLadoPorQuadrado(object, d):
    andar_em_metros(object, d, 5, 0.20)
    
def TurnInSquare(object, angle):  # gira no centro do quadrado e vai para ponta
    print(angle)

    alinhar(object)
    MoveDirectionPosition(object, 2, 0.065)
    if(angle > 0):
        direcaoEGiro(object, abs(angle))
    if(angle < 0):
        direcaoEGiro(object, abs(angle))
    MoveDirectionPosition(object, 8, 0.025)
    alinhar(object)
        
def MoveDirectionPosition(direcao, dist):  # Andar reto para frente ou para trás
    andar_em_metros(direcao, 5, dist)

# def inicio_virar_SUL(): #para a função COM VISÃO

#     d=0

#     while(True):

#         erro,b=sim.simxGetObjectOrientation(glob.clientID,glob.robo,-1,sim.simx_opmode_blocking)
#         gamma=(b[2]*180)/(np.pi)

#         if(gamma>=-3 and gamma<=3):
#             Stop()
#             break

#         if(d==0):
#             if(gamma>0 and gamma<179.99):
#                 d = 1
#             else:
#                 d = -1

#         v=4
#         sim.simxPauseCommunication(glob.clientID, True)
#         sim.simxSetJointTargetVelocity(glob.clientID,glob.robotRightMotor,d*v, sim.simx_opmode_oneshot)
#         sim.simxSetJointTargetVelocity(glob.clientID,glob.robotLeftMotor,(-1)*d*v, sim.simx_opmode_oneshot)
#         sim.simxPauseCommunication(glob.clientID, False)

#     align.Align()
#     andar_em_metros(tras, 5, 0.065)
#     return

# def inicio_virar_NORTE(): #para a função SEM VISÃO; lembrar de adicionar no if(nao viu prataleira) virar 180.

#     d=0

#     while(True):

#         erro,b=sim.simxGetObjectOrientation(glob.clientID,glob.robo,-1,sim.simx_opmode_blocking)
#         gamma=(b[2]*180)/(np.pi)

#         if(gamma>=177 or gamma<=-177):
#             Stop()
#             break

#         if(d==0):
#             if(gamma>0 and gamma<179.99):
#                 d = 1
#             else:
#                 d =-1

#         v=4
#         sim.simxPauseCommunication(glob.clientID, True)
#         sim.simxSetJointTargetVelocity(glob.clientID,glob.robotRightMotor,d*v, sim.simx_opmode_oneshot)
#         sim.simxSetJointTargetVelocity(glob.clientID,glob.robotLeftMotor,(-1)*d*v, sim.simx_opmode_oneshot)
#         sim.simxPauseCommunication(glob.clientID, False)

#     align.Align()
#     return



