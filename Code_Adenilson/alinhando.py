import sim
import numpy as np
import time
import simConst
from girar import *
from motor import *
from sensor import *
from object_handle import *

#Função de alinhamento #############################

def alinhar():
        while True:
            esquerda = Ler_Cor(adeni, 'esquerda')
            direita = Ler_Cor(adeni, 'direita')
            if esquerda =='PRETO' or direita =='preto':
                print('quebrei')
                break
            else:
                print('to andando')
                move_frente(adeni,3)
        while True:
            flag = 0
            corE =Ler_Cor(adeni, 'esquerda')
            corD = Ler_Cor(adeni, 'direita')
            if flag:
                break
            while Ler_Cor(adeni, 'esquerda')== 'PRETO' and Ler_Cor(adeni, 'direita') == 'BRANCO':
                print('cor esquerda PRETO')
                giro_livre(adeni, 1,1)
                flag =1
            while Ler_Cor(adeni, 'esquerda') == 'BRANCO' and Ler_Cor(adeni, 'direita') == 'PRETO':
                print('cor direita PRETA')
                giro_livre(adeni, -1,1)
                flag = 1
            else:
                move_frente(adeni, 3)
    #while True:
     #   alinhar()
        
    # while True:
    # turn_around_angle(adeni, 100, 1, 2)
    # girar_90_graus(adeni, 1)

    # girar_90_graus(adeni, 1)

    # giro_livre(adeni,1,2)
    # andar_em_metros(adeni, 'tras', 2, 1)
    #while girando<1:
     #   alinhar
    