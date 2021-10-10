import sim
import time
import numpy as np
import cv2
def getImage(object, _camera):
	errol = 1

	while(errol != sim.simx_return_ok):
		errol, res, image = sim.simxGetVisionSensorImage(object.clientID, _camera, 0, sim.simx_opmode_buffer)
		time.sleep(0.005)
	nres = [res[0]-int(res[0]/3),res[1]]
	img = np.array(image, dtype=np.uint8)		# Como é recebido uma string, precisa reformatar
	img = np.reshape(img, (res[0], res[1], 3))	# Pro CV2, (y, x, [B,R,G])
	img = np.flip(img, 0)						# Por algum motivo vem de ponta cabeça
	img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)	# Transforma o RGB recebido em BGR pro CV2
	img = img[0:res[0]-(int(res[0]/3)), 0:res[1]]


	cv2.imwrite('./imgs/0src.png', img)
	return img, nres

def basicFilter(_src):
	"Processamento basico para isolar as cores do fim"
	#Isolar a cores procuradas usando HSV:
	hsv = cv2.cvtColor(_src, cv2.COLOR_BGR2HSV)

	hsv_lower = np.array([0,200,200])
	hsv_upper = np.array([179,255,255])
	mask = cv2.inRange(hsv, hsv_lower, hsv_upper)

	#Copiar a mascara para a imagem inicial:
	_src2 = _src.copy()
	img = cv2.bitwise_and(_src, _src, mask=mask)

	#Transformar para cinza:
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cv2.imwrite('./imgs/1gray.png', img)

	# Media:
	img = cv2.medianBlur(img, 3)
	cv2.imwrite('./imgs/4median.png', img)

	cv2.namedWindow('image')
	cv2.imshow('image',img)
	cv2.waitKey()

	nimg = img.copy()

	return nimg

def compareCenters(_cx, _cy, _centers):
	"Compara os valores [cy,cx] com o vetor 2d conhecido"
	if(len(_centers) == 0):
		return 1
	for coord in _centers:
		if(abs(coord[0] - _cy) > 5 or abs(coord[1] - _cx) > 5):
			pass
		else:
			return 0
	return 1

def findUseful(_src, _img):
	"Acha os contornos uteis da imagem"
	#Pega todas as bordas por Canny:
	thres, _img = cv2.threshold(_img, 10, 255, cv2.THRESH_BINARY)
	edges = cv2.Canny(_img, 100, 200)
	cv2.imwrite('./imgs/5edges.png', edges)
	foundCenters = np.empty(shape=[0,2])

	foundColors = np.empty(shape=[0,3])
	shapeArea = np.empty(shape=[0])
	errorim = _src.copy()


	#Aproxima os possiveis contornos:
	contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	for cnt in contours:
		#Pega o tamanho:
		perimeter = cv2.arcLength(cnt, True)

		#Grava os centros:
		m = cv2.moments(cnt)
		if (m['m00'] == 0):
			m['m00'] = 1
		cx = int(m['m10']/m['m00'])
		cy = int(m['m01']/m['m00'])

		if(compareCenters(cx, cy, foundCenters) == 1):
			if(perimeter > 160 and perimeter < 1200):
				#print(perimeter)
				k = np.array([[[cx,cy]]])

				foundCenters = np.append(foundCenters, [[cy,cx]], axis=0)
				foundColors = np.append(foundColors, [_src[cy][cx]], axis=0)
				cv2.drawContours(_src, k, -1, (255,0,255), 3)
			else:
				print(perimeter)
				#print("A")
				cv2.drawContours(errorim, cnt, -1, (255,255,0), 3)
		else:
			cv2.drawContours(errorim, cnt, -1, (255,0,255), 3)

	cv2.imwrite('./imgs/8centers.png', _src)
	cv2.imwrite('./imgs/0errors.png', errorim)
	cv2.namedWindow('image')
	cv2.imshow('image',_src)
	cv2.waitKey()
	cv2.imshow('image',errorim)
	cv2.waitKey()
	#print(foundCenters)
	#print(foundColors)
	return foundColors, foundCenters

def getMostCentered(_res, _centers):
	most = 1000
	num = 0

	#print(_centers)
	#print(_res[1]/2)
	for center in _centers:
		if(abs(center[1] - _res[1]/2) < most):
			choice = num
			#print(choice)
			most = abs(center[1] - _res[1]/2)
		num = num + 1

	most = 1000
	num = 0
	choice2 = -1
	for center in _centers:
		if(abs(center[1] - _centers[choice][1]) < most and center[1] > _centers[choice][1]):
			choice2 = num
			most = abs(center[1] - _centers[choice][1])
		num = num + 1

	return choice, choice2

def rgbToLetter(_colors):
	if(_colors[0] > 100 and _colors[1] > 100):
		newColors = 'W'
	elif(_colors[0] > 100):
		newColors = 'B'
	elif(_colors[1] > 100 and _colors[2] > 100):
		newColors = 'Y'
	elif(_colors[1] > 100):
		newColors = 'G'
	elif(_colors[2] < 100):
		newColors = 'K'
	else:
		newColors = 'R'
	return newColors

def test(camera):

	image, resol = getImage(camera)

	# Create a window
	cv2.namedWindow('image')
	cv2.namedWindow('track')

	boundaries = [
		([17, 15, 100], [50, 56, 200]),
		([86, 31, 4], [220, 88, 50]),
		([25, 146, 190], [62, 174, 250]),
		([103, 86, 65], [145, 133, 128])
	]

	# create trackbars for color change
	cv2.createTrackbar('HMin','track',0,179,nothing) # Hue is from 0-179 for Opencv
	cv2.createTrackbar('SMin','track',0,255,nothing)
	cv2.createTrackbar('VMin','track',0,255,nothing)
	cv2.createTrackbar('HMax','track',0,179,nothing)
	cv2.createTrackbar('SMax','track',0,255,nothing)
	cv2.createTrackbar('VMax','track',0,255,nothing)

	# Set default value for MAX HSV trackbars.
	cv2.setTrackbarPos('HMax', 'track', 179)
	cv2.setTrackbarPos('SMax', 'track', 255)
	cv2.setTrackbarPos('VMax', 'track', 255)

	# Initialize to check if HSV min/max value changes
	hMin = sMin = vMin = hMax = sMax = vMax = 0
	phMin = psMin = pvMin = phMax = psMax = pvMax = 0

	output = image
	wait_time = 33

	#for (lower, upper) in boundaries:
	#	# create NumPy arrays from the boundaries
	#	lower = np.array(lower, dtype = "uint8")
	#	upper = np.array(upper, dtype = "uint8")
	#	# find the colors within the specified boundaries and apply
	#	# the mask
	#	mask = cv2.inRange(image, lower, upper)
	#	output = cv2.bitwise_and(image, image, mask = mask)
	#	# show the images
	#	cv2.imshow("images", np.hstack([image, output]))
	#	cv2.waitKey(0)

	while(1):
		frame, resol = getImage(camera)
		# get current positions of all trackbars
		hMin = cv2.getTrackbarPos('HMin','track')
		sMin = cv2.getTrackbarPos('SMin','track')
		vMin = cv2.getTrackbarPos('VMin','track')

		hMax = cv2.getTrackbarPos('HMax','track')
		sMax = cv2.getTrackbarPos('SMax','track')
		vMax = cv2.getTrackbarPos('VMax','track')

		# Set minimum and max HSV values to display
		lower = np.array([hMin, sMin, vMin])
		upper = np.array([hMax, sMax, vMax])

		# Create HSV Image and threshold into a range.
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		mask = cv2.inRange(hsv, lower, upper)
		output = cv2.bitwise_and(image,image, mask= mask)

		# Print if there is a change in HSV value
		if( (phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
			print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
			phMin = hMin
			psMin = sMin
			pvMin = vMin
			phMax = hMax
			psMax = sMax
			pvMax = vMax

		# Display output image
		cv2.imshow('image',output)

		# Wait longer to prevent freeze for videos.
		if cv2.waitKey(wait_time) & 0xFF == ord('q'):
			break

	cv2.destroyAllWindows()

def getX(_colorSet, _edge):
	if(_colorSet[0] == 'R'):
		return 3
	elif(_colorSet[0] == 'Y' and _colorSet[1] == 'R'):
		return 4
	elif(_colorSet[0] == 'Y'):
		return 2
	elif(_colorSet[0] == 'B' and _colorSet[1] == 'Y'):
		return 5
	elif(_colorSet[0] == 'B'):
		return 1
	elif(_colorSet[0] == 'G' and _edge != -1):
		return 6
	else:
		return 0

def getY(_center, _res):
	percent = _center[0] / _res[0]
	print(percent)
	if(percent > 0.7):#0.72
		return 5
	elif(percent > 0.6):#0.64
		return 4
	elif(percent > 0.35):#0.37
		return 3
	elif(percent > 0.2):#0.22
		return 2
	elif(percent > 0.10):#0.11
		return 1
	else:#>0.16
		return 0

def identifyFirstPos(object):
	global sigValue


	camera = object.camera_superior
	# Start the Stream
	erro, res, image = sim.simxGetVisionSensorImage(object.clientID, camera, 0, sim.simx_opmode_streaming)
	frame, resol = getImage(object, camera)
	#test(camera)

	filtered = basicFilter(frame)
	foundColors, foundCenters = findUseful(frame.copy(), filtered)

	if(foundCenters.size == 0):
		return 0, -1

	center, right = getMostCentered(resol, foundCenters)
	#print(center, right)
	colors = [rgbToLetter(foundColors[center]), rgbToLetter(foundColors[right])]
	while(colors[0] != 'G' and right == -1):
		frame, resol = getImage(object, camera)
		filtered = basicFilter(frame)
		foundColors, foundCenters = findUseful(frame.copy(), filtered)
		center, right = getMostCentered(resol, foundCenters)
		colors = [rgbToLetter(foundColors[center]), rgbToLetter(foundColors[right])]

	return getY(foundCenters[center], resol), getX(colors, right)
