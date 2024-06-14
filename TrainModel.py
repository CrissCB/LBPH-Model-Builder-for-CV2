import shutil
import cv2
import os
import numpy as np
import time

def get_model(method,facesData,labels, route, name, master, text):
	if method == 'EigenFaces': emotion_recognizer = cv2.face.EigenFaceRecognizer_create() # type: ignore
	if method == 'FisherFaces': emotion_recognizer = cv2.face.FisherFaceRecognizer_create() # type: ignore
	if method == 'LBPH': emotion_recognizer = cv2.face.LBPHFaceRecognizer_create() # type: ignore

	# Entrenando el reconocedor de rostros
	text += "\nEntrenando ( "+method+" )..."
	master.info_label(text)
	inicio = time.time()
	emotion_recognizer.train(facesData, np.array(labels))
	tiempoEntrenamiento = time.time()-inicio
	text += "\nTiempo de entrenamiento ( "+method+" ): "+str(tiempoEntrenamiento)
	master.info_label(text)

	# Guardar el modelo entrenado
	model_file = os.path.join(route, name+method+".xml")
	emotion_recognizer.write(model_file)

	# Guardar el txt con las emociones
	try:
        # Copiar el archivo
		new_name = os.path.join(route, name+method+".txt")
		shutil.copy('data/emotion_List.txt', new_name)
	except Exception as e:
		print(e)

	text += '\nokay, method '+method+' trained'
	master.info_label(text) 

def init_model(emotionsList, route, name, master):
	text = 'Lista de Emociones: '+str(emotionsList)
	master.info_label(text)
	dataPath = 'data/emotions'

	labels = []
	facesData = []
	label = 0

	for nameDir in emotionsList:
		emotionsPath = dataPath + '/' + nameDir

		for fileName in os.listdir(emotionsPath):
			labels.append(label)
			facesData.append(cv2.imread(emotionsPath+'/'+fileName,0))

		label = label + 1
	
	print(labels)

	get_model('LBPH',facesData,labels, route, name, master, text)