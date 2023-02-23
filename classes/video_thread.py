from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QUrl
import simpleaudio as sa
import cv2
import numpy as np

from models.model_detector import ObjDetector
import config
	
class VideoThread(QThread):
	change_pixmap_signal = pyqtSignal(cv2.VideoCapture, np.ndarray)
	object_detected_signal = pyqtSignal(cv2.VideoCapture, np.ndarray, str)
	
	
	def run(self):
		self.model = ObjDetector()
		self.model.loadModels()
		self.model.startCapture(self.onVideoAcquired, self.onFrameRead, self.onObjDetected)
	
	def pause(self):
		self.model.pause = True
		
	def resume(self):
		self.model.pause = False
	
	def togglePause(self):
		self.model.pause = False if self.model.pause else True
		
	def stop(self):
		self.model.stop = True
		
	def onVideoAcquired(self, cap):
		pass
		
	def onObjDetected(self, cap, frame, objType):
		self.object_detected_signal.emit(cap, frame, objType)
		# self.playSound(config.BASE_DIR + "/audios/persona-detectada.wav")
		
	def onFrameRead(self, cap, frame):
		self.change_pixmap_signal.emit(cap, frame)
		
	def playSound(self, filename):
		print('Reproduciendo audio: {0}'.format(filename))
		wave_obj = sa.WaveObject.from_wave_file(filename)
		play_obj = wave_obj.play()
		play_obj.wait_done()
