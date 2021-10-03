import sim
import numpy as np
import time

import sim
#from motor import stop

## FUNÇÕES DE GIRAR ######################################


def stop(object):
    sim.simxPauseCommunication(object.clientID, True)
    print(sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_direita_frente, 0, sim.simx_opmode_oneshot))
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_direita_atras, 0, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_esquerda_frente, 0, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_esquerda_atras, 0, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)
    time.sleep(0.5)


def giro_livre(object, d, v):
    # d = 1 , horario
    # d =-1 , anti
    # v = velocidade
    sim.simxPauseCommunication(object.clientID, True)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_direita_frente, d * v * (-1), sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_esquerda_frente, d * v * (-1), sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_direita_atras, d * v * (-1), sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(
        object.clientID, object.omniWheel_esquerda_atras, d * v * (-1), sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(object.clientID, False)


def get_angle_that_makes_sense(object):
    erro, euler_angles = sim.simxGetObjectOrientation(
        object.clientID, object.robot, -1, sim.simx_opmode_streaming)
    while (erro != 0):
        erro, euler_angles = sim.simxGetObjectOrientation(
            object.clientID, object.robot, -1, sim.simx_opmode_streaming)

    print(erro, euler_angles)
    factor = 90
    # print(factor)
    if (euler_angles[0] <= 0):
        factor = 270
    # print(factor)
    print((np.sign(euler_angles[1]) * 60*euler_angles[2]))
    finalAngle = (np.sign(euler_angles[1]) * 60 * euler_angles[2]) + factor
    return finalAngle


def turn_around_angle(object, angle, sentido, velocidade):
    # sentido = 1 roda em sentido antihorario
    # sentido = -1 roda em sentido horario
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


def girar_180_graus(object):
    girar_90_graus(object, 1)
    girar_90_graus(object, 1)

# gira no sentido horário sem nenhum problema, porém no anti horario apresenta problemas.
def girar_90_graus(object, sentido):
    # sentido = 1 , anti horario, esquerda
    # sentido =-1 , horario, direita

    velocidade = 2  # se velocidade = 5, passo = 3.4
    passo = 1.5

    angulo_inicial = get_angle_that_makes_sense(object)

    # Começa a girar, talvez de para trocar essas linhas por: giro_livre(object, sentido, velocidade)
    giro_livre(object, sentido, velocidade)
    # print("ANTES DO WHILE", sentido)
    while True:
        angulo_final = get_angle_that_makes_sense(object)

        angulo_percorrido = angulo_final - angulo_inicial

        if sentido == 1:  # anti horário
            print("To aqui -> ", angulo_percorrido, " - ",
                  angulo_final, " - ", angulo_inicial)
            if angulo_percorrido < 0:  # estava no 4º quadrante e foi para o 1º
                angulo_percorrido += 360  # transforma para um ângulo positivo na primeira volta
        elif sentido != 1:  # horário
            # como está no sentido horário os valores vão vir negativos, ai multiplica por -1 pra arrumar
            angulo_percorrido *= -1
            if angulo_percorrido < 0:  # estava no 1º quadrante e foi para o 4º
                angulo_percorrido += 360  # transforma para um ângulo positivo na primeira volta
        # print("dps DO WHILE", type(sentido))

        # implementar aquilo que a gente falou do controle de velocidade baseado no quão próximo o robô está do ângulo final

        if (86) < angulo_percorrido < (96):
            # print(50*'#')
            print("Final angulo_percorrido: ", angulo_percorrido)  # teste
            # print(50*'#')
            break
    stop(object)
