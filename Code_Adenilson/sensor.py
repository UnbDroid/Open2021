import sim
import numpy as np
from object_handle import ObjectHandle


def Ler_Cor(object, direction):
    if direction.lower() == "esquerda":
        sensor_cor = object.cor_esquerda
    elif direction.lower() == "direita":
        sensor_cor = object.cor_direita
    elif direction.lower() == "esquerdacosta":
        sensor_cor = object.cor_esquerda_costas
    elif direction.lower() == "direitacosta":
        sensor_cor = object.cor_direita_costas
    elif direction.lower() == "direitalateral1":
        sensor_cor = object.cor_direita_lateral1
    elif direction.lower() == "esquerdalateral1":
        sensor_cor = object.cor_esquerda_lateral1
    elif direction.lower() == "direitalateral2":
        sensor_cor = object.cor_direita_lateral2
    elif direction.lower() == "esquerdalateral2":
        sensor_cor = object.cor_esquerda_lateral2
    elif direction.lower() == "aux":
        sensor_cor = object.color_sensor_aux
    else:
        print("NÃO DEU BOM")
        # sensor_cor = object.color_sensor_front
    erro, resolution, Image = sim.simxGetVisionSensorImage(
        object.clientID, sensor_cor, 0, sim.simx_opmode_streaming)
    while (erro != 0):
        erro, resolution, Image = sim.simxGetVisionSensorImage(
            object.clientID, sensor_cor, 0, sim.simx_opmode_buffer)

    img = np.array(Image, dtype=np.uint8)
    min_color_value = 200
    rgb_color = 0
    if (img[0] > min_color_value):
        rgb_color += 100
    if (img[1] > min_color_value):
        rgb_color += 10
    if (img[2] > min_color_value):
        rgb_color += 1
    if (rgb_color == 1):
        return 'AZUL'
    if (rgb_color == 10):
        return 'VERDE'
    if (rgb_color == 100):
        return 'VERMELHO'
    if (rgb_color == 110):
        return 'AMARELO'
    if (rgb_color == 111):
        return 'BRANCO'
    return 'PRETO'


def Ler_Distancia(object, direction):
    if direction.lower() == "costas":
        sensor_us = object.us_costas
    elif direction.lower() == "direita":
        sensor_us = object.us_direita
    max_distance = 1

    erro, detectionState, distancePoint, detectedObjectHandle, detectedSurface = sim.simxReadProximitySensor(
        object.clientID, sensor_us, sim.simx_opmode_streaming)
    while (erro != 0):
        erro, detectionState, distancePoint, detectedObjectHandle, detectedSurface = sim.simxReadProximitySensor(
            object.clientID, sensor_us, sim.simx_opmode_buffer)
    # print(erro, detectionState, distancePoint, detectedObjectHandle, detectedSurface)
    if(detectionState == False):
        distance = max_distance
    else:
        distance = distancePoint[2]

    return distance


def read_force(object):

    erro, state, forceVector, torqueVector = sim.simxReadForceSensor(
        object.clientID, object.force_sensor, sim.simx_opmode_streaming)
    while (erro != 0):
        erro, state, forceVector, torqueVector = sim.simxReadForceSensor(
            object.clientID, object.force_sensor, sim.simx_opmode_buffer)
    print("erro:", erro, "state", state, "forceVector",
          forceVector, "torqueVector", torqueVector)
    return forceVector[2]


def getCubeHandle(object, sensor):
    erro = 1
    while (erro != 0):
        erro, detectionState, distancePoint, detectedObjectHandle, detectedSurface = sim.simxReadProximitySensor(
            object.clientID, sensor, sim.simx_opmode_streaming)
    return detectedObjectHandle


def le_distancia_ir(object, sensor):
    max_distance_IR = 1
    erro = 1
    while (erro != 0): 
        erro, detectable, distancePoint, detectedObjectHandle, detectedSurface = sim.simxReadProximitySensor(object.clientID, sensor, sim.simx_opmode_streaming)
    distance = distancePoint[2]
    if(detectable == False):
        distance = max_distance_IR
    return distance
