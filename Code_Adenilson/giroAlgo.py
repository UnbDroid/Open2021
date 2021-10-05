# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

try:
    import sim
except:
    print ('--------------------------------------------------------------')
    print ('"sim.py" could not be imported. This means very probably that')
    print ('either "sim.py" or the remoteApi library could not be found.')
    print ('Make sure both are in the same folder as this file,')
    print ('or appropriately adjust the file "sim.py"')
    print ('--------------------------------------------------------------')
    print ('')

import time
import numpy as np

def Stop(clientID, _robotRightMotor, _robotLeftMotor):
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID, _robotRightMotor, 0, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID, _robotLeftMotor, 0, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

def Girar_X_graus(clientID, _robotRightMotor, _robotLeftMotor, _robo, d, graus):
    
    # d = 1 , anti horario, esquerda
    # d =-1 , horario, direita
    # v = velocidade
    
    v = 5
    g = graus
    erro,b_inicial=sim.simxGetObjectOrientation(clientID,_robo,-1,sim.simx_opmode_streaming)
    while(erro != 0):
        erro,b_inicial=sim.simxGetObjectOrientation(clientID,_robo,-1,sim.simx_opmode_streaming)


    gamma_inicial=b_inicial[2]*180/(np.pi)
    gamma_target=gamma_inicial-g*d
    if(abs(gamma_target) > 190):
        gamma_target = d*g
        
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID,_robotRightMotor,d*v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID,_robotLeftMotor,(-1)*d*v, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

    while(True):
        erro,b=sim.simxGetObjectOrientation(clientID,_robo,-1,sim.simx_opmode_buffer)
        gamma=b[2]*180/(np.pi)
 
        #print(gamma)
        if(abs(abs(gamma)-abs(gamma_inicial))>=0.85*g):
            break
        
        #print(gamma_inicial,gamma)
    Stop(clientID, _robotRightMotor, _robotLeftMotor)
    erro,b_inicial=sim.simxGetObjectOrientation(clientID,_robo,-1,sim.simx_opmode_buffer)
    #gamma_inicial=b_inicial[2]*180/(np.pi)

    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID,_robotRightMotor,d*0.5, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID,_robotLeftMotor,(-1)*d*0.5, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

    #print(gamma_inicial,gamma_target,gamma)
    while(True):
        sign = np.sign(gamma)
        erro,b=sim.simxGetObjectOrientation(clientID,_robo,-1,sim.simx_opmode_buffer)
        gamma=b[2]
        gamma=gamma*180/(np.pi)

        #print(gamma)
        if(d*(gamma-gamma_target) < 0 or np.sign(gamma) != sign):
            break
        
    #print(gamma_inicial,gamma)
    Stop(clientID, _robotRightMotor, _robotLeftMotor)

def Girar_90_graus_v2(clientID, _robotRightMotor, _robotLeftMotor, _robo, d):

    # d = 1 , anti horario, esquerda
    # d =-1 , horario, direita
    # v = velocidade
    
    v = 5
    g = 90
    erro,b_inicial=sim.simxGetObjectOrientation(clientID,_robo,-1,sim.simx_opmode_streaming)
    while(erro != 0):
        erro,b_inicial=sim.simxGetObjectOrientation(clientID,_robo,-1,sim.simx_opmode_streaming)


    gamma_inicial=b_inicial[2]*180/(np.pi)
    gamma_target=gamma_inicial-g*d
    if(abs(gamma_target) > 190):
        gamma_target = d*g
        
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID,_robotRightMotor,d*v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID,_robotLeftMotor,(-1)*d*v, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

    while(True):
        erro,b=sim.simxGetObjectOrientation(clientID,_robo,-1,sim.simx_opmode_buffer)
        gamma=b[2]*180/(np.pi)
 
        #print(gamma)
        if(abs(abs(gamma)-abs(gamma_inicial))>=0.85*g):
            break
        
        #print(gamma_inicial,gamma)
    Stop(clientID, _robotRightMotor, _robotLeftMotor)
    erro,b_inicial=sim.simxGetObjectOrientation(clientID,_robo,-1,sim.simx_opmode_buffer)
    #gamma_inicial=b_inicial[2]*180/(np.pi)

    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID,_robotRightMotor,d*0.5, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID,_robotLeftMotor,(-1)*d*0.5, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

    #print(gamma_inicial,gamma_target,gamma)
    while(True):
        sign = np.sign(gamma)
        erro,b=sim.simxGetObjectOrientation(clientID,_robo,-1,sim.simx_opmode_buffer)
        gamma=b[2]
        gamma=gamma*180/(np.pi)

        #print(gamma)
        if(d*(gamma-gamma_target) < 0 or np.sign(gamma) != sign):
            break
        
    #print(gamma_inicial,gamma)
    Stop(clientID, _robotRightMotor, _robotLeftMotor)


def Girar_180_graus_v2(clientID, _robotRightMotor, _robotLeftMotor, _robo): 

    v = 8
    g = 90
    d = 1
    erro,b_inicial=sim.simxGetObjectOrientation(clientID,_robo,-1,sim.simx_opmode_streaming)
    while(erro != 0):
        erro,b_inicial=sim.simxGetObjectOrientation(clientID,_robo,-1,sim.simx_opmode_streaming)


    gamma_inicial=b_inicial[2]*180/(np.pi)
    gamma_target=gamma_inicial-g*2
    if(abs(gamma_target) > 190):
        gamma_target = gamma_inicial + 180
    if(gamma_inicial <= 100 and gamma_inicial > -80):
        d = 0
        
    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID,_robotRightMotor,v, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID,_robotLeftMotor,(-1)*v, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

    #print(gamma_inicial)
    while(True):
        erro,b=sim.simxGetObjectOrientation(clientID,_robo,-1,sim.simx_opmode_buffer)
        gamma=b[2]*180/(np.pi)
 
        #print(gamma)
        if(gamma <= gamma_target+15 and d and np.sign(gamma) == 1):
            break
        if(gamma <= gamma_target+15 and not d and np.sign(gamma) == -1):
            break
        
        #print(gamma_inicial,gamma)
    Stop(clientID, _robotRightMotor, _robotLeftMotor)
    erro,b_inicial=sim.simxGetObjectOrientation(clientID,_robo,-1,sim.simx_opmode_buffer)
    #gamma_inicial=b_inicial[2]*180/(np.pi)

    sim.simxPauseCommunication(clientID, True)
    sim.simxSetJointTargetVelocity(clientID,_robotRightMotor,0.5, sim.simx_opmode_oneshot)
    sim.simxSetJointTargetVelocity(clientID,_robotLeftMotor,(-1)*0.5, sim.simx_opmode_oneshot)
    sim.simxPauseCommunication(clientID, False)

    #print(gamma_inicial,gamma_target,gamma)
    while(True):
        sign = np.sign(gamma)
        erro,b=sim.simxGetObjectOrientation(clientID,_robo,-1,sim.simx_opmode_buffer)
        gamma=b[2]
        gamma=gamma*180/(np.pi)

        #print(gamma)
        if(gamma-gamma_target < 0 or np.sign(gamma) != sign):
            break
        
    #print(gamma_inicial,gamma)
    Stop(clientID, _robotRightMotor, _robotLeftMotor)