import sim
import time

NORTE = 1
SUL = -1
LESTE = 2
OESTE = -2
axisX = 0
axisY = 1
frente = 8
tras = 2
direita = 1
esquerda = -1


class ObjectHandle:
   def __init__(self, clientID, robotname):
      self.clientID = clientID
      self.robotname = robotname
      self.cubo_garra_frente = 'HELLO' #0 se estiver vazio, se tiver cubo botar o número dele
      self.cubo_garra_costas = 'HELLLOOOOK' #0 se estiver vazio, se tiver cubo botar o número dele

      ######## Robô:
      erro, self.robot = sim.simxGetObjectHandle(self.clientID, self.robotname, sim.simx_opmode_blocking)
      erro, self.s_base = sim.simxGetObjectHandle(self.clientID, 'S_Base', sim.simx_opmode_blocking)

      ####### OmniWheels:
      erro, self.omniWheel_direita_frente = sim.simxGetObjectHandle(self.clientID, 'OmniWheel_Direita_Frente', sim.simx_opmode_blocking)
      erro, self.omniWheel_direita_atras = sim.simxGetObjectHandle(self.clientID, 'OmniWheel_Direita_Atras', sim.simx_opmode_blocking)
      erro, self.omniWheel_esquerda_frente = sim.simxGetObjectHandle(self.clientID, 'OmniWheel_Esquerda_Frente', sim.simx_opmode_blocking)
      erro, self.omniWheel_esquerda_atras = sim.simxGetObjectHandle(self.clientID, 'OmniWheel_Esquerda_Atras', sim.simx_opmode_blocking)
      erro, self.junta_deslizadorad_df = sim.simxGetObjectHandle(self.clientID, 'slippingJoint_Direita_Frente', sim.simx_opmode_blocking)
      erro, self.junta_deslizadora_da = sim.simxGetObjectHandle(self.clientID, 'slippingJoint_Direita_Atras', sim.simx_opmode_blocking)
      erro, self.junta_deslizadora_ef = sim.simxGetObjectHandle(self.clientID, 'slippingJoint_Esquerda_Frente', sim.simx_opmode_blocking)
      erro, self.junta_deslizadora_ea = sim.simxGetObjectHandle(self.clientID, 'slippingJoint_Esquerda_Atras', sim.simx_opmode_blocking)

      ####### Garras:
      erro, self.acoplador_garra1 = sim.simxGetObjectHandle(self.clientID,'joint_acoplador_garra1',sim.simx_opmode_blocking) #garra 1 => frente
      erro, self.acoplador_garra2 = sim.simxGetObjectHandle(self.clientID,'joint_acoplador_garra2',sim.simx_opmode_blocking) #garra 2 => costas
      erro, self.cubo_acoplador1 = sim.simxGetObjectHandle(self.clientID,'Cuboid_acoplador',sim.simx_opmode_blocking)
      erro, self.cubo_acoplador2 = sim.simxGetObjectHandle(self.clientID,'Cuboid_acoplador#0',sim.simx_opmode_blocking)
      erro, self.pa_direita1 = sim.simxGetObjectHandle(self.clientID,'joint_pa_direita_garra1',sim.simx_opmode_blocking)
      erro, self.pa_esquerda1 = sim.simxGetObjectHandle(self.clientID,'joint_pa_esquerda_garra1',sim.simx_opmode_blocking)
      erro, self.pa_direita2 = sim.simxGetObjectHandle(self.clientID,'joint_pa_direita_garra2',sim.simx_opmode_blocking)
      erro, self.pa_esquerda2 = sim.simxGetObjectHandle(self.clientID,'joint_pa_esquerda_garra2',sim.simx_opmode_blocking)

      ######### Sensores:
      erro, self.us_costas = sim.simxGetObjectHandle(self.clientID, 'Sensor_US_Costas', sim.simx_opmode_blocking)
      erro, self.us_direita = sim.simxGetObjectHandle(self.clientID, 'Sensor_US_Direita', sim.simx_opmode_blocking)
      erro, self.cor_esquerda  = sim.simxGetObjectHandle(self.clientID, 'Sensor_cor_esquerda', sim.simx_opmode_blocking)
      erro, self.cor_direita = sim.simxGetObjectHandle(self.clientID, 'Sensor_cor_direita', sim.simx_opmode_blocking)
      erro, self.camera_chao = sim.simxGetObjectHandle(self.clientID, 'Camera_Inferior_Chao', sim.simx_opmode_blocking)
      erro, self.camera_superior = sim.simxGetObjectHandle(self.clientID, 'Camera_Superior_Vision', sim.simx_opmode_blocking)
      erro, self.cor_esquerda_lateral1  = sim.simxGetObjectHandle(self.clientID, 'Sensor_cor_lateral_direita1', sim.simx_opmode_blocking)
      erro, self.cor_direita_lateral1 = sim.simxGetObjectHandle(self.clientID, 'Sensor_cor_lateral_direita', sim.simx_opmode_blocking)
      erro, self.cor_esquerda_lateral2  = sim.simxGetObjectHandle(self.clientID, 'Sensor_cor_lateral_esquerda1', sim.simx_opmode_blocking)
      erro, self.cor_direita_lateral2 = sim.simxGetObjectHandle(self.clientID, 'Sensor_cor_lateral_esquerda', sim.simx_opmode_blocking)
      erro, self.cor_esquerda_costas  = sim.simxGetObjectHandle(self.clientID, 'Sensor_cor_costas_esquerda', sim.simx_opmode_blocking)
      erro, self.cor_direita_costas = sim.simxGetObjectHandle(self.clientID, 'Sensor_cor_costas_direita', sim.simx_opmode_blocking)
      erro, self.ir_frente_direita = sim.simxGetObjectHandle(self.clientID, 'Sensor_IR_frente_direita', sim.simx_opmode_blocking)
      erro, self.ir_frente_esquerda = sim.simxGetObjectHandle(self.clientID, 'Sensor_IR_frente_esquerda', sim.simx_opmode_blocking)
      erro, self.ir_costas_direita = sim.simxGetObjectHandle(self.clientID, 'Sensor_IR_costas_direita', sim.simx_opmode_blocking)
      erro, self.ir_costas_esquerda = sim.simxGetObjectHandle(self.clientID, 'Sensor_IR_costas_esquerda', sim.simx_opmode_blocking)
