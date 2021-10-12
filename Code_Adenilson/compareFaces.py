import cv2
import numpy as np

def compareNumber(_compImg, _compRes):
	num = 0
	match = [0,10]
	print(_compRes)
	cv2.imshow('compass',_compImg)
	while(num < 15):
		ret = 0
		imgt =   "./Cubes/" + str(num) + ".png"
		imgNum = cv2.imread(imgt,0)
		imgNum = cv2.resize(imgNum, (_compRes[1],_compRes[0]))

		contSrc, hier = cv2.findContours(imgNum, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		contCmp, hier = cv2.findContours(_compImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		imgNum = cv2.cvtColor(imgNum, cv2.COLOR_GRAY2BGR)

		for this in range(len(contSrc)):
			if(this > len(contCmp)-1):
				break
			perSrc = cv2.arcLength(contSrc[this], True)
			perCmp = cv2.arcLength(contCmp[this], True)
			if(perSrc < 500 and perCmp < 500):
				ret = ret + cv2.matchShapes(contCmp[this], contSrc[this], 3, 0.0)

		if(len(contCmp) != len(contSrc)):
			ret = ret + 0.5



		if(match[1] > ret):
			for cnt in contCmp:
				cv2.drawContours(imgNum, cnt, -1, (255,0,255), 3)
			for cnt in contSrc:
				cv2.drawContours(imgNum, cnt, -1, (0,255,255), 3)
			cv2.imwrite('./imgs/AA.png', imgNum)
			match[0] = num
			match[1] = ret

		num = num + 1

	return match


def compareBar(_compImg, _compRes):
	match = [0,0,0,0]


	cv2.imwrite('./imgs/AB.png', _compImg)

	for x in range(4):
		img = _compImg.copy()
		cv2.imwrite('./imgs/AB' + str(x) + '.png', img)
		img = img[int(_compRes[0]*0.2):int(_compRes[0]*0.8), int(_compRes[1]*(0.1+(0.1*2*x))):int(_compRes[1]*(0.3+(0.1*2*x)))]
		cv2.imwrite('./imgs/AA' + str(x) + '.png', img)
		avg = np.average(img)
		match[x] = 1 if(avg > 127) else 0

	print(match)
	match.reverse()
	strings = [str(integer) for integer in match]
	a_string = "".join(strings)
	match = int(a_string, 2)

	return match
