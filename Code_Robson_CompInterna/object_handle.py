import sim

class ObjectHandle:
    def __init__(self, clientID,robotname):
        self.clientID = clientID
        self.robotname = robotname
     #Robô
    	erro, self.robot = sim.simxGetObjectHandle(self.clientID, self.robotname, sim.simx_opmode_blocking)
    	erro, self.s_base = sim.simxGetObjectHandle(self.clientID, 'S_Base', sim.simx_opmode_blocking)
     #OmniWheels:
        erro, self.omniWheel_direita_frente = sim.simxGetObjectHandle(self.clientID, 'OmniWheel_Direita_Frente', sim.simx_opmode_blocking)
        erro, self.omniWheel_direita_atras = sim.simxGetObjectHandle(self.clientID, 'OmniWheel_Direita_Atras', sim.simx_opmode_blocking)
        erro, self.omniWheel_esquerda_frente = sim.simxGetObjectHandle(self.clientID, 'OmniWheel_Esquerda_Frente', sim.simx_opmode_blocking)
        erro, self.omniWheel_esquerda_atras = sim.simxGetObjectHandle(self.clientID, 'OmniWheel_Esquerda_Atras', sim.simx_opmode_blocking)
        erro, self.junta_deslizadorad_df = sim.simxGetObjectHandle(self.clientID, 'slippingJoint_Direita_Frente', sim.simx_opmode_blocking)
        erro, self.junta_deslizadora_da = sim.simxGetObjectHandle(self.clientID, 'slippingJoint_Direita_Atras', sim.simx_opmode_blocking)
        erro, self.junta_deslizadora_ef = sim.simxGetObjectHandle(self.clientID, 'slippingJoint_Esquerda_Frente', sim.simx_opmode_blocking)
        erro, self.junta_deslizadora_ea = sim.simxGetObjectHandle(self.clientID, 'slippingJoint_Esquerda_Atras', sim.simx_opmode_blocking)
     #Garras:
        erro, self.acoplador_garra1 = sim.simxGetObjectHandle(self.clientID,'joint_acoplador_garra1',sim.simx_opmode_blocking)
        erro, self.acoplador_garra2 = sim.simxGetObjectHandle(self.clientID,'joint_acoplador_garra2',sim.simx_opmode_blocking)
        erro, self.pa_direita1 = sim.simxGetObjectHandle(self.clientID,'joint_pa_direita_garra1',sim.simx_opmode_blocking)
        erro, self.pa_esquerda1 = sim.simxGetObjectHandle(self.clientID,'joint_pa_direita_garra1',sim.simx_opmode_blocking)
        erro, self.pa_direita2 = sim.simxGetObjectHandle(self.clientID,'joint_pa_direita_garra2',sim.simx_opmode_blocking)
        erro, self.pa_esquerda2 = sim.simxGetObjectHandle(self.clientID,'joint_pa_direita_garra2',sim.simx_opmode_blocking)
     #Sensores:
        erro, self.us_frente = sim.simxGetObjectHandle(self.clientID, 'Sensor_US_Frente', sim.simx_opmode_blocking)
        erro, self.us_lateral = sim.simxGetObjectHandle(self.clientID, 'Sensor_US_Lateral', sim.simx_opmode_blocking)
        erro, self.cor_esquerda = sim.simxGetObjectHandle(self.clientID, 'Sensor_cor_esquerda', sim.simx_opmode_blocking)
        erro, self.cor_direita = sim.simxGetObjectHandle(self.clientID, 'Sensor_cor_direita', sim.simx_opmode_blocking)
        erro, self.camera_chao = sim.simxGetObjectHandle(self.clientID, 'Camera_Inferior_Chao', sim.simx_opmode_blocking)
        erro, self.camera_superior = sim.simxGetObjectHandle(self.clientID, 'Camera_Superior_Vision', sim.simx_opmode_blocking)