# coding=utf-8
# Insert in a script in Coppelia

import sim
import globalDefs as glob
from globalDefs import *
import sensorAlgo as sense
import locomAlgo as move
import numpy as np

def Align():   #em desenvolvimento
    v = 2
    direita_preto = False
    esquerda_preto = False
    sim.simxGetObjectPosition(glob.clientID, glob.color_sensor_Left, -1, sim.simx_opmode_streaming)
    sim.simxGetObjectPosition(glob.clientID, glob.color_sensor_Right, -1, sim.simx_opmode_streaming)

    while(True):

        if (sense.getColor(glob.color_sensor_Left) == PRETO or sense.getColor(glob.color_sensor_Right) == PRETO):
            #print("To procurando a linha")
            #print("Achei pela primeira vez")
            break

        move.MoveForward(v)

    move.Stop()
    [erro, pri_pos_cor_dir] = sim.simxGetObjectPosition(glob.clientID, glob.color_sensor_Right, -1, sim.simx_opmode_buffer)
    #print(erro, pri_pos_cor_dir)
    [erro, pri_pos_cor_esq] = sim.simxGetObjectPosition(glob.clientID, glob.color_sensor_Left, -1, sim.simx_opmode_buffer)
    #print(erro, pri_pos_cor_esq)

    if (sense.getColor(glob.color_sensor_Left) == PRETO):
        esquerda_preto = True

        while(True):

            if (sense.getColor(glob.color_sensor_Right) == PRETO):
                #print("Achei pela segunda vez direito")
                break

            move.MoveForward(v)

    elif (sense.getColor(glob.color_sensor_Right) == PRETO):
        direita_preto = True

        while(True):

            if (sense.getColor(glob.color_sensor_Left) == PRETO):
                #print("Achei pela segunda vez esquerdo")
                break

            move.MoveForward(v)

    move.Stop()
    [erro, seg_pos_cor_dir] = sim.simxGetObjectPosition(glob.clientID, glob.color_sensor_Right, -1, sim.simx_opmode_buffer)
    #print(erro, seg_pos_cor_dir)
    [erro, seg_pos_cor_esq] = sim.simxGetObjectPosition(glob.clientID, glob.color_sensor_Left, -1, sim.simx_opmode_buffer)
    #print(erro, seg_pos_cor_esq)
    #A essa altura, o robô já andou, viu a linha com o primeiro sensor, andou mais e viu a linha com o segundo

    linha_vertical = False
    linha_horizontal = False

    x_p_dif_trans = np.abs(pri_pos_cor_dir[0] - pri_pos_cor_esq[0])
    x_s_dif_trans = np.abs(seg_pos_cor_dir[0] - seg_pos_cor_esq[0])
    x_e_dif_longi = np.abs(pri_pos_cor_esq[0] - seg_pos_cor_esq[0])
    x_d_dif_longi = np.abs(pri_pos_cor_dir[0] - seg_pos_cor_dir[0])

    y_p_dif_trans = np.abs(pri_pos_cor_dir[1] - pri_pos_cor_esq[1])
    y_s_dif_trans = np.abs(seg_pos_cor_dir[1] - seg_pos_cor_esq[1])
    y_e_dif_longi = np.abs(pri_pos_cor_esq[1] - seg_pos_cor_esq[1])
    y_d_dif_longi = np.abs(pri_pos_cor_dir[1] - seg_pos_cor_dir[1])


        ######################################################################
        ##### TABELA EXPLICATIVA #####
        #Essa tabela vale para x e para y, mas separadamente
        #S*n = "sensor" + lado (d=direita, e=esquerda) + vez que viu a linha (1a ou 2a)
        #dif = diferenca
        #trans = transversal (sempre compara direita e esquerda)
        #longi = longitudinal (sempre compara o mesmo lado)
        #cruz = cruzada (existe e eh diferente de zero, mas nao sera utilizada)
        #p = primeira (1a = 1), s = segunda (2a = 2)
        #
        #    |      SE1      |      SD1      |      SE2      |      SD2      |
        #SE1 |       0       |  p_dif_trans  |  e_dif_longi  | -ed_dif_cruz- |
        #SD1 |  p_dif_trans  |       0       | -de_dif_cruz- |  d_dif_longi  |
        #SE2 |  e_dif_longi  | -de_dif_cruz- |       0       |  s_dif_trans  |
        #SD2 | -ed_dif_cruz- |  d_dif_longi  |  s_dif_trans  |       0       |



    if(x_s_dif_trans > y_s_dif_trans):
        #print('desalinhado horizontal')
        linha_horizontal = True

        if (esquerda_preto == True):

            if(y_e_dif_longi > 1):
                print("Estou descentralizado para a esquerda")
                #criar funcao que recentraliza
            else:
                while(True):

                    [erro, atual_pos_cor_esq] = sim.simxGetObjectPosition(glob.clientID, glob.color_sensor_Left, -1, sim.simx_opmode_buffer)
                    ye_atual_dif_longi = np.abs(seg_pos_cor_esq[1] - atual_pos_cor_esq[1])

                    if(int(ye_atual_dif_longi*1000000) >= int(y_s_dif_trans*1000000)):
                        # print("Alinhando")
                        # print("Alinhei")
                        # print(int(ye_atual_dif_longi*100000))
                        # print(int(y_s_dif_trans*100000))
                        break

                    move.gira_livre_uma_roda(esquerda, 1, 0.3)



        elif (direita_preto == True):

            if(y_d_dif_longi > 1):
                print("Estou descentralizado para a direita")
                #criar funcao que recentraliza
            else:
                while(True):

                    [erro, atual_pos_cor_dir] = sim.simxGetObjectPosition(glob.clientID, glob.color_sensor_Right, -1, sim.simx_opmode_buffer)
                    yd_atual_dif_longi = np.abs(seg_pos_cor_dir[1] - atual_pos_cor_dir[1])

                    if(int(yd_atual_dif_longi*1000000) >= int(y_s_dif_trans*1000000)):
                        # print("Alinhando")
                        # print("Alinhei")
                        # print(int(yd_atual_dif_longi*1000000))
                        # print(int(y_s_dif_trans*1000000))
                        break

                    move.gira_livre_uma_roda(direita, -1, 0.3)


    elif(x_s_dif_trans < y_s_dif_trans):
        # print('desalinhado vertical')
        linha_vertical = True

        if (esquerda_preto == True):

            if (x_e_dif_longi > 1):
                print("Estou descentralizado para a esquerda")
                # criar funcao que recentraliza
            else:
                while (True):

                    [erro, atual_pos_cor_esq] = sim.simxGetObjectPosition(glob.clientID, glob.color_sensor_Left, -1, sim.simx_opmode_buffer)
                    xe_atual_dif_longi = np.abs(seg_pos_cor_esq[0] - atual_pos_cor_esq[0])

                    if (int(xe_atual_dif_longi*1000000) >= int(x_s_dif_trans*1000000)):
                        # print("Alinhando")
                        # print("Alinhei")
                        # print(int(xe_atual_dif_longi*1000000))
                        # print(int(x_s_dif_trans*1000000))
                        break

                    move.gira_livre_uma_roda(esquerda, 1, 0.3)

        elif (direita_preto == True):

            if (x_d_dif_longi > 1):
                print("Estou descentralizado para a direita")
                # criar funcao que recentraliza
            else:
                while (True):

                    [erro, atual_pos_cor_dir] = sim.simxGetObjectPosition(glob.clientID, glob.color_sensor_Right, -1, sim.simx_opmode_buffer)
                    xd_atual_dif_longi = np.abs(seg_pos_cor_dir[0] - atual_pos_cor_dir[0])

                    if (int(xd_atual_dif_longi*1000000) >= int(x_s_dif_trans*1000000)):
                        # print("Alinhando")
                        # print("Alinhei")
                        # print(xd_atual_dif_longi)
                        # print(x_s_dif_trans)
                        break

                    move.gira_livre_uma_roda(direita, -1, 0.3)




    move.Stop()
    # print("Parei de girar")

    # if (sense.getColor(glob.color_sensor_Left) != PRETO):
    #     print("Esquerdo branco")
    # else:  # (sense.getColor(glob.color_sensor_Right) == PRETO):
    #     print("Esquerdo preto")
    # if (sense.getColor(glob.color_sensor_Right) != PRETO):
    #     print("Direito branco")
    # else:  # (sense.getColor(glob.color_sensor_Left) == PRETO):
    #     print("Direito preto")


def AlignBack(v):
    while (sense.getColor(glob.color_sensor_Left) != PRETO or sense.getColor(glob.color_sensor_Right) != PRETO):
        move.MoveBack(v)
    move.Stop()

def AlignSpecial(v):
    leftLine = True
    rightLine = True
    while (leftLine or rightLine):
        if(sense.getColor(glob.color_sensor_Left) == PRETO):
            leftLine = False
        if(sense.getColor(glob.color_sensor_Right) == PRETO):
            rightLine = False
        move.MoveForward(v)
    move.Stop()