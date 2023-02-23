# -*- coding: utf-8 -*-
import cv2
import config
import time

class ObjDetector:

	def __init__(self):
		# Class labels
		self.classes = {
			0: "background", 
			1: "avion", 
			2: "bicicleta",
			3: "pajaro", 
			4: "boat",
			5: "bottle", 
			6: "bus",
			7: "automovil", 
			8: "gato",
			9: "silla", 
			10: "vaca",
			11: "diningtable", 
			12: "perro",
			13: "caballo", 
			14: "motorbike",
			15: "persona", 
			16: "pottedplant",
			17: "sheep", 
			18: "sofa",
			19: "tren", 
			20: "tv o monitor"
		}
		self.protxt = None
		self.model = None
		self.net = None
		self.pause = False
		self.stop = False
		
	def loadModels(self):
		# ----------- READ DNN MODEL -----------
		# Model architecture
		self.prototxt = config.BASE_DIR + "/ai_models/MobileNetSSD_deploy.prototxt.txt"
		# Weights
		self.model = config.BASE_DIR + "/ai_models/MobileNetSSD_deploy.caffemodel"
		# Load the model
		self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)
		
	def processImage(self):
		# ----------- READ THE IMAGE AND PREPROCESSING -----------
		image = cv2.imread("ImagesVideos/imagen_0004.jpg")
		
		height, width, _ = image.shape
		image_resized = cv2.resize(image, (300, 300))
		# Create a blob
		blob = cv2.dnn.blobFromImage(image_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5))
		print("blob.shape:", blob.shape)
		# ----------- DETECTIONS AND PREDICTIONS -----------
		net.setInput(blob)
		detections = net.forward()
		for detection in detections[0][0]:
			print(detection)
			if detection[2] > 0.45:
				label = classes[detection[1]]
				print("Label:", label)
				box = detection[3:7] * [width, height, width, height]
				x_start, y_start, x_end, y_end = int(box[0]), int(box[1]), int(box[2]), int(box[3])
				cv2.rectangle(image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
				cv2.putText(image, "Conf: {:.2f}".format(detection[2] * 100), (x_start, y_start - 5), 1, 1.2, (255, 0, 0), 2)
				cv2.putText(image, label, (x_start, y_start - 25), 1, 1.2, (255, 0, 0), 2)
		cv2.imshow("Image", image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	def startCapture(self, callbackVideoAcquired=None, callbackFrameRead=None, callbackObjDetected=None):
		# ----------- READ THE IMAGE AND PREPROCESSING -----------
		#cap = cv2.VideoCapture("ImagesVideos/video_0004.mp4")
		#cap = cv2.VideoCapture("http://192.168.0.24:4747/video/override")
		cap = cv2.VideoCapture("/Users/marcelo/Movies/mixkit-professional-programmer-working-on-a-big-computer-41642-medium.mp4")
		# cap = cv2.VideoCapture("http://192.168.0.25:8080/video")
		# cv2.namedWindow('Main Window WebCam', cv2.WINDOW_NORMAL)
		if callbackVideoAcquired is not None:
			callbackVideoAcquired(cap)
			
		while True:
			if self.pause is True:
				time.sleep(1)
				continue
				
			if self.stop is True:
				break
				
			ret, frame, = cap.read()
			if ret == False:
				break
			# print(type(cap), type(frame))
			#quit()
			if callbackFrameRead is not None:
				callbackFrameRead(cap, frame)
				
			height, width, _ = frame.shape
			frame_resized = cv2.resize(frame, (300, 300))
			# Create a blob
			blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5))
			#print("blob.shape:", blob.shape)
			# ----------- DETECTIONS AND PREDICTIONS -----------
			self.net.setInput(blob)
			detections = self.net.forward()
			
			for detection in detections[0][0]:
				#print(detection)
				if detection[2] > 0.45:
					label = self.classes[detection[1]]
					print("Objeto detectado:", label)
					box = detection[3:7] * [width, height, width, height]
					x_start, y_start, x_end, y_end = int(box[0]), int(box[1]), int(box[2]), int(box[3])
					cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
					cv2.putText(frame, "Conf: {:.2f}".format(detection[2] * 100), (x_start, y_start - 5), 1, 1.2, (255, 0, 0), 2)
					cv2.putText(frame, label, (x_start, y_start - 25), 1, 1.5, (0, 255, 255), 2)
					if callbackObjDetected is not None:
						callbackObjDetected(cap, frame, label)
					
			# cv2.imshow("Frame", frame)
			if cv2.waitKey(1) & 0xFF == 27:
				break
		
		cap.release()
		cv2.destroyAllWindows()
