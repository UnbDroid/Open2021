import sim
import numpy as np
import time
import simConst
from girar import *
from sensor import *

## FUNÇÕES DE LOCOMOÇAO ######################################


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
        object.clientID, object.omniWheel_direita_frente, v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_direita_atras, v, sim.simx_opmode_oneshot)
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

    # d = 1 direita
    # d =-1 esquerda
    if d == 1:
        variacao = 0.915
    elif d == -1:
        variacao = 0.78
    # v = velocidade

    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_direita_frente, -v*variacao*d, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_esquerda_frente, -v*d, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_direita_atras, +v*variacao*d, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_esquerda_atras, +v*d, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)

def andar_em_metros(object, d, v, m): #anda em todos os sentidos dependendo da direção
    # d = frente, andar para frente
    # d = tras, andar para trás
    # d = esquerda, andar para esquerda
    # d = direita, andar para direita
    # v = velocidade
    # m = valor em metros

    erro, a_inicial = sim.simxGetObjectPosition(
        object.clientID, object.robot, -1, sim.simx_opmode_blocking)
    x_inicial = a_inicial[0]
    y_inicial = a_inicial[1]

    if d == 'frente':
        move_frente(object, v)
    if d == 'tras':
        move_tras(object, v)
    if d == 'esquerda':
        andar_livre(object, -1, v)
    if d == 'direita':
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

def alinharLateral(object, d):#alinha lateral esquerda e direita
    velocidade = 5
    if d == 'direita':
        valSensorEsquerdo = 'esquerdaLateral1'
        valSensorDireito = 'direitaLateral1'
        d = 1
    elif d == 'esquerda':
        valSensorEsquerdo = 'esquerdaLateral2'
        valSensorDireito = 'direitaLateral2'
        d = -1

    while True:
        if velocidade>=2:
            velocidade-=0.0005
        
        esquerda = Ler_Cor(object, valSensorEsquerdo)
        direita = Ler_Cor(object, valSensorDireito)
        if esquerda == 'PRETO' or direita == 'PRETO':
            # print('quebrei')
            stop(object)
            # print('dei um break')
            break
        else:
            # print('to andando')
            andar_livre(object, d, velocidade)
    print(velocidade)
    flag = 0
    while True:

        corE = Ler_Cor(object, valSensorEsquerdo)
        # print("COR ESQUERDA LATERAL == ", corE)
        corD = Ler_Cor(object, valSensorDireito)
        # print("COR DIREITA LATERAL == ", corD)

        # if flag:
        #     break
        if corE == 'PRETO' and corD == 'PRETO':
            break
        if corE == 'BRANCO' and corD == 'BRANCO':
            andar_livre(object, d, 3)
        while Ler_Cor(object, valSensorEsquerdo) == 'PRETO' and Ler_Cor(object, valSensorDireito) == 'BRANCO':
            # print('cor esquerda PRETO')
            giro_livre(object, d, 1)
            flag = 1
        while Ler_Cor(object, valSensorEsquerdo) == 'BRANCO' and Ler_Cor(object, valSensorDireito) == 'PRETO':
            # print('cor direitaLateral PRETA')
            giro_livre(object, d*-1, 1)
            flag = 1
        # else:
            # andar_livre(object, d, 2)
    stop(object)

def alinharComLateralFT(object, d, canto): #alinha frente e costas.
    if d == 'frente':
        valSensorEsquerdo = 'direitalateral2'
        valSensorDireito = 'direitalateral1'
    elif d == 'tras':
        valSensorEsquerdo = 'esquerdalateral2'
        valSensorDireito = 'esquerdalateral1'

    while True:
        esquerda = Ler_Cor(object, valSensorEsquerdo)
        direita = Ler_Cor(object, valSensorDireito)
        if esquerda == 'PRETO' or direita == 'PRETO':
            # print('quebrei')
            # print('dei um break2')
            stop(object)
            break

        else:
            # print('to andando')
            if d == 'tras':
                move_tras(object, 2.5)
            else:
                move_frente(object, 2.5)
    flag = 0
    while True:

        corE = Ler_Cor(object, valSensorEsquerdo)
        # print("COR ESQUERDA == ", corE)
        corD = Ler_Cor(object, valSensorDireito)
        # print("COR DIREITA == ", corD)

        # if flag:
        #     break
        if corE == 'PRETO' and corD == 'PRETO':
            break
        if corE == 'BRANCO' and corD == 'BRANCO':
            break
        while Ler_Cor(object, valSensorEsquerdo) == 'PRETO' and Ler_Cor(object, valSensorDireito) == 'BRANCO':
            # print('cor esquerda PRETO')
            giro_livre(object, canto, 1.3)
            flag = 1
        while Ler_Cor(object, valSensorEsquerdo) == 'BRANCO' and Ler_Cor(object, valSensorDireito) == 'PRETO':
            # print('cor direita PRETA')
            giro_livre(object, -canto, 1.3)
            flag = 1
        # else:
        # move_frente(object, 3)
    stop(object)
    return get_angle_that_makes_sense(object)



def alinhar(object, d): #alinha frente e costas.
    velocidade = 5
    if d == 'frente':
        valSensorEsquerdo = 'esquerda'
        valSensorDireito = 'direita'
    elif d == 'tras':
        valSensorEsquerdo = 'esquerdacosta'
        valSensorDireito = 'direitacosta'

    while True:
        if velocidade>=2:
            velocidade-=0.0005
        esquerda = Ler_Cor(object, valSensorEsquerdo)
        direita = Ler_Cor(object, valSensorDireito)
    
        if esquerda == 'PRETO' or direita == 'PRETO':
            # print('quebrei')
            # print('dei um break2')
            stop(object)
            break

        else:
            # print('to andando')
            if d == 'tras':
                move_tras(object, velocidade)
            else:
                move_frente(object, velocidade)
    print(velocidade)
    
    flag = 0
    while True:

        corE = Ler_Cor(object, valSensorEsquerdo)
        # print("COR ESQUERDA == ", corE)
        corD = Ler_Cor(object, valSensorDireito)
        # print("COR DIREITA == ", corD)

        # if flag:
        #     break
        if corE == 'PRETO' and corD == 'PRETO':
            break
        if corE == 'BRANCO' and corD == 'BRANCO':
            break
        while Ler_Cor(object, valSensorEsquerdo) == 'PRETO' and Ler_Cor(object, valSensorDireito) == 'BRANCO':
            # print('cor esquerda PRETO')
            giro_livre(object, -1, 1.3)
            flag = 1
        while Ler_Cor(object, valSensorEsquerdo) == 'BRANCO' and Ler_Cor(object, valSensorDireito) == 'PRETO':
            # print('cor direita PRETA')
            giro_livre(object, 1, 1.3)
            flag = 1
        # else:
        # move_frente(object, 3)
    stop(object)

def direcaoEGiro(object, ang): #girar para a direita ou para a esquerda pelo angulo que você escolher

    if (ang == 180):
        # print("EAE BRIWBS")
        # pass
        #turn_around_angle(object, 180, -1, 3.60)
        girar_90_graus(object, 1)
        # girar_90_graus(object, -1)
        # print("EAE 222222")

    else:
        # print("EAE BASDASDASDAS")
        # pass
        girar_90_graus(object, 1)

def MoveForwardPosition(object, dist):
    MoveDirectionPosition(object, 8, dist)

def moverPorQuadrado(object, d): #move frente ou trás dependendo da direção
    andar_em_metros(object, d, 6, 0.16)
    alinhar(object, d)
    if d == 'tras':
        andar_em_metros(object, 'frente', 2, 0.02)
    elif d == 'frente':
        andar_em_metros(object, 'tras', 2, 0.02)

def moverLadoPorQuadrado(object, d): #move direita ou esquerda dependendo da direção
    andar_em_metros(object, d, 5, 0.16)
    alinharLateral(object, d)
    if d == 'direita':
        andar_em_metros(object, 'esquerda', 2, 0.02)
    elif d == 'esquerda':
        andar_em_metros(object, 'direita', 2, 0.02)

def TurnInSquare(object, angle):  #gira no centro do quadrado e vai para ponta
    # print(angle)

    alinhar(object, 'frente')
    MoveDirectionPosition( 2, 0.065)
    if(angle > 0):
        direcaoEGiro(object, abs(angle))
    if(angle < 0):
        direcaoEGiro(object, abs(angle))
    MoveDirectionPosition( 8, 0.025)
    alinhar(object)

def MoveDirectionPosition(direcao, dist ):  #andar reto para frente ou para trás
    andar_em_metros(object,direcao, 5, dist)

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
