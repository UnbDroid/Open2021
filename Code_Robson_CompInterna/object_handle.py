import sim

class ObjectHandle:
    def __init__(self, clientID,robotname):
        self.clientID = clientID
        self.robotname = robotname

    def handle_Robot(self):
    	erro, self.robot = sim.simxGetObjectHandle(self.clientID, self.robotname, sim.simx_opmode_blocking)
    	erro, self.S_Base = sim.simxGetObjectHandle(self.clientID, 'S_Base', sim.simx_opmode_blocking)

    def handle_OmniWheels(self):
        erro, self.OmniWheel_Direita_Frente = sim.simxGetObjectHandle(self.clientID, 'OmniWheel_Direita_Frente', sim.simx_opmode_blocking)
        erro, self.OmniWheel_Direita_Atras = sim.simxGetObjectHandle(self.clientID, 'OmniWheel_Direita_Atras', sim.simx_opmode_blocking)
        erro, self.OmniWheel_Esquerda_Frente = sim.simxGetObjectHandle(self.clientID, 'OmniWheel_Esquerda_Frente', sim.simx_opmode_blocking)
        erro, self.OmniWheel_Esquerda_Atras = sim.simxGetObjectHandle(self.clientID, 'OmniWheel_Esquerda_Atras', sim.simx_opmode_blocking)
        erro, self.junta_deslizadoraDF = sim.simxGetObjectHandle(self.clientID, 'slippingJoint_Direita_Frente', sim.simx_opmode_blocking)
        erro, self.junta_deslizadoraDA = sim.simxGetObjectHandle(self.clientID, 'slippingJoint_Direita_Atras', sim.simx_opmode_blocking)
        erro, self.junta_deslizadoraEF = sim.simxGetObjectHandle(self.clientID, 'slippingJoint_Esquerda_Frente', sim.simx_opmode_blocking)
        erro, self.junta_deslizadoraEA = sim.simxGetObjectHandle(self.clientID, 'slippingJoint_Esquerda_Atras', sim.simx_opmode_blocking)

    def handle_Garras(self):
        erro, self.acoplador_garra1 = sim.simxGetObjectHandle(self.clientID,'joint_acoplador_garra1',sim.simx_opmode_blocking)
        erro, self.acoplador_garra2 = sim.simxGetObjectHandle(self.clientID,'joint_acoplador_garra2',sim.simx_opmode_blocking)
        erro, self.pa_direita1 = sim.simxGetObjectHandle(self.clientID,'joint_pa_direita_garra1',sim.simx_opmode_blocking)
        erro, self.pa_esquerda1 = sim.simxGetObjectHandle(self.clientID,'joint_pa_direita_garra1',sim.simx_opmode_blocking)
        erro, self.pa_direita2 = sim.simxGetObjectHandle(self.clientID,'joint_pa_direita_garra2',sim.simx_opmode_blocking)
        erro, self.pa_esquerda2 = sim.simxGetObjectHandle(self.clientID,'joint_pa_direita_garra2',sim.simx_opmode_blocking)

    def handle_Sensores(self):
        erro, self.us_frente = sim.simxGetObjectHandle(self.clientID, 'Sensor_US_Frente', sim.simx_opmode_blocking)
        erro, self.us_lateral = sim.simxGetObjectHandle(self.clientID, 'Sensor_US_Lateral', sim.simx_opmode_blocking)
        erro, self.cor_esquerda = sim.simxGetObjectHandle(self.clientID, 'Sensor_cor_esquerda', sim.simx_opmode_blocking)
        erro, self.cor_direita = sim.simxGetObjectHandle(self.clientID, 'Sensor_cor_direita', sim.simx_opmode_blocking)
        erro, self.camera_chao = sim.simxGetObjectHandle(self.clientID, 'Camera_Inferior_Chao', sim.simx_opmode_blocking)
        erro, self.camera_superior = sim.simxGetObjectHandle(self.clientID, 'Camera_Superior_Vision', sim.simx_opmode_blocking)