# coding=utf-8
import numpy as np


def inicio_virar_SUL(): # para a função COM VISÃO
    
    d=0

    while(True):
        
        erro,b=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
        gamma=(b[2]*180)/(np.pi)

        if(gamma>=-3 and gamma<=3):
            Stop()
            break

        if(d==0):
            if(gamma>0 and gamma<179.99):
                d = -1
            else:
                d = 1

        v=4
        sim.simxPauseCommunication(clientID, True)
        sim.simxSetJointTargetVelocity(clientID,robotRightMotor,d*v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(clientID,robotLeftMotor,(-1)*d*v, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(clientID, False)

    Align()
    return

def inicio_virar_NORTE(): # para a função SEM VISÃO; lembrar de adicionar no if(nao viu prataleira) virar 180.

    d=0

    while(True):
        
        erro,b=sim.simxGetObjectOrientation(clientID,robo,-1,sim.simx_opmode_blocking)
        gamma=(b[2]*180)/(np.pi)

        if(gamma>=177 or gamma<=-177):
            Stop()
            break

        if(d==0):
            if(gamma>0 and gamma<179.99):
                d = 1
            else:
                d =-1
        
        v=4
        sim.simxPauseCommunication(clientID, True)
        sim.simxSetJointTargetVelocity(clientID,robotRightMotor,d*v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(clientID,robotLeftMotor,(-1)*d*v, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(clientID, False)

    Align()
    return

