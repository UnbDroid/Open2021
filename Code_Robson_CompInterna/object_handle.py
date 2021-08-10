import sim

class ObjectHandle:
    def __init__(self, clientID,robotname):
        self.clientID = clientID
        self.robotname = robotname

    def handle_robot(self):
    	erro, self.robot = sim.simxGetObjectHandle(self.clientID, self.robotname, sim.simx_opmode_blocking)
    	erro, self.bloco_frente = sim.simxGetObjectHandle(self.clientID, 'Bloco_frente', sim.simx_opmode_blocking)

    def handle_wheels(self):
        erro, self.robotBackLeftMotor = sim.simxGetObjectHandle(self.clientID, 'Revolute_joint1', sim.simx_opmode_blocking)
        erro, self.robotFrontLeftMotor = sim.simxGetObjectHandle(self.clientID, 'Revolute_joint2', sim.simx_opmode_blocking)
        erro, self.robotFrontRightMotor = sim.simxGetObjectHandle(self.clientID, 'Revolute_joint3', sim.simx_opmode_blocking)
        erro, self.robotBackRightMotor = sim.simxGetObjectHandle(self.clientID, 'Revolute_joint4', sim.simx_opmode_blocking)

    def handle_arms(self):
        erro, self.leftArmFrente = sim.simxGetObjectHandle(self.clientID,'Prismatic_joint4',sim.simx_opmode_blocking)
        erro, self.rightArmFrente = sim.simxGetObjectHandle(self.clientID,'Prismatic_joint3',sim.simx_opmode_blocking)
        erro, self.leftArmTras = sim.simxGetObjectHandle(self.clientID,'Prismatic_joint2',sim.simx_opmode_blocking)
        erro, self.rightArmTras = sim.simxGetObjectHandle(self.clientID,'Prismatic_joint1',sim.simx_opmode_blocking)

    def handle_sensors(self):
        erro, self.us_front = sim.simxGetObjectHandle(self.clientID, 'Sensor_us_frente', sim.simx_opmode_blocking)
        erro, self.us_back = sim.simxGetObjectHandle(self.clientID, 'Sensor_us_tras', sim.simx_opmode_blocking)
        erro, self.us_left = sim.simxGetObjectHandle(self.clientID, 'Sensor_us_esq', sim.simx_opmode_blocking)
        erro, self.us_right = sim.simxGetObjectHandle(self.clientID, 'Sensor_us_dir', sim.simx_opmode_blocking)
        erro , self.color_sensor_left = sim.simxGetObjectHandle(self.clientID, 'Sensor_cor_esq', sim.simx_opmode_blocking)
        erro , self.color_sensor_right = sim.simxGetObjectHandle(self.clientID, 'Sensor_cor_dir', sim.simx_opmode_blocking)
        erro , self.color_sensor_aux = sim.simxGetObjectHandle(self.clientID, 'Sensor_cor_auxiliar', sim.simx_opmode_blocking)
        erro , self.color_sensor_front = sim.simxGetObjectHandle(self.clientID, 'Sensor_cor_frente', sim.simx_opmode_blocking)
        erro , self.force_sensor = sim.simxGetObjectHandle(self.clientID, 'ForceSensor', sim.simx_opmode_blocking)
        erro , self.teste = sim.simxGetObjectHandle(self.clientID, 'Cuboid7', sim.simx_opmode_blocking)
