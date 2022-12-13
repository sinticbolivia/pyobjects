from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QUrl
import simpleaudio as sa
import cv2
import numpy as np

from models.model_detector import ObjDetector
import config
	
class VideoThread(QThread):
	change_pixmap_signal = pyqtSignal(cv2.VideoCapture, np.ndarray)
	object_detected_signal = pyqtSignal(cv2.VideoCapture, np.ndarray)
	
	def run(self):
		model = ObjDetector()
		model.loadModels()
		model.startCapture(self.onVideoAcquired, self.onFrameRead, self.onObjDetected)
		
	def onVideoAcquired(self, cap):
		pass
		
	def onObjDetected(self, cap, frame):
		self.object_detected_signal.emit(cap, frame)
		# self.playSound(config.BASE_DIR + "/audios/persona-detectada.wav")
		
	def onFrameRead(self, cap, frame):
		self.change_pixmap_signal.emit(cap, frame)
		
	def playSound(self, filename):
		print('Reproduciendo audio: {0}'.format(filename))
		wave_obj = sa.WaveObject.from_wave_file(filename)
		play_obj = wave_obj.play()
		play_obj.wait_done()
