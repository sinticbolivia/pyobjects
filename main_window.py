# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton)
from PyQt6.QtGui import QPixmap, QImage, QPixmap
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QUrl, QSize
from PyQt6.QtMultimedia import QSoundEffect, QAudioOutput, QMediaPlayer
import cv2
import numpy as np

from classes.video_thread import VideoThread
import config


video_image_label = None
image_label = None
display_width = 450
display_height = 450
window = None

def demo_sound(filename):
	print('Reproduciendo audio: {0}'.format(filename))
	player = QMediaPlayer()
	#'''
	audio_output = QAudioOutput()
	player.setAudioOutput(audio_output)
	player.setSource(QUrl.fromLocalFile(filename))
	audio_output.setVolume(50)
	#'''
	player.play()
	
def convert_cv_qt(cap, frame):
	"""Convert from an opencv image to QPixmap"""
	
	rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	h, w, ch = rgb_image.shape
	bytes_per_line = ch * w
	# convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888) ## Qt5
	# p = convert_to_Qt_format.scaled(display_width, display_height, Qt.KeepAspectRatio) ## Qt5
	convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
	p = convert_to_Qt_format.scaled(display_width, display_height, Qt.AspectRatioMode.KeepAspectRatio)
	
	return QPixmap.fromImage(p)
	
@pyqtSlot(np.ndarray)
def update_video(cap, frame):
	global video_image_label
	
	qt_img = convert_cv_qt(cap, frame)
	video_image_label.setPixmap(qt_img)
	
@pyqtSlot(np.ndarray)
def update_image(cap, frame, objType):
	global image_label
	#from app import window
	qt_img = convert_cv_qt(cap, frame)
	image_label.setPixmap(qt_img)
	# demo_sound( config.BASE_DIR + "/audios/persona-detectada.mp3" )
	window.set_counter(objType)
		
# class MainWindow(QMainWindow):
class MainWindow(QWidget):
	# video_image_label	= None
	#image_label = None
	current_user = None
	
	def __init__(self):
		super().__init__()
		# import app
		# from app import current_user
		self.setWindowTitle('Sistema de Control')
		
		self.leftContainer = QVBoxLayout()
		self.rightContainer = QVBoxLayout()
		self.container		= None
		self.buttonsGrid	= None
		# self.buttonRegistrar	= None
		self.buttonIniciar		= None
		self.buttonPausar		= None
		self.buttonDetener		= None
		self.buttonGrabar		= None
		self.buttonHistorial	= None
		self.buttonReportes		= None
		self.video_image_label	= QLabel()
		self.video_image_label.resize(300, 300)
		self.image_label = QLabel()
		self.image_label.resize(300, 300)
		self.thread = None
		
		self.labelPersonCount = None;
		self.labelCarCount = None
		self.labelMCCount = None
		self.labelAnimalCount = None
		
		self.build()
		
	def build(self):
		global video_image_label, image_label, window
		
		self.container = QVBoxLayout()
		topContainer = QHBoxLayout()
		pixmapLogo = QPixmap('{0}/images/EjercitoEB.png'.format(config.BASE_DIR))
		labelPixmapLogo = QLabel('')
		labelPixmapLogo.setPixmap(pixmapLogo.scaled(QSize(80, 80), Qt.AspectRatioMode.KeepAspectRatio))
		labelPixmapLogo1 = QLabel('')
		labelPixmapLogo1.setPixmap(pixmapLogo.scaled(QSize(80, 80), Qt.AspectRatioMode.KeepAspectRatio))
		
		labelTitle = QLabel('Algoritmos para la identificacion de movimientos en la linea fronteriza e hitos militares,\n en el control de puntos de ingreso a Bolivia')
		labelTitle.setProperty('class', 'title')
		labelTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
		topContainer.addWidget( labelPixmapLogo )
		topContainer.addWidget(labelTitle)
		topContainer.addWidget( labelPixmapLogo1 )
		
		colsContainer = QHBoxLayout()
		colsContainer.addLayout(self.leftContainer)
		colsContainer.addLayout(self.rightContainer)
		self.buttonsGrid = QGridLayout()
		
		# self.leftContainer.addWidget(QPushButton('Left Button'))
		self.leftContainer.addLayout(self.build_objects_counter())
		self.leftContainer.addLayout(self.buttonsGrid)
		
		# self.buttonRegistrar = QPushButton('Registrar')
		self.buttonIniciar = QPushButton('Iniciar')
		self.buttonIniciar.setProperty('class', 'btn-primary')
		self.buttonPausar = QPushButton('Pausar')
		self.buttonPausar.setProperty('class', 'btn-warning')
		self.buttonDetener = QPushButton('Detener')
		self.buttonDetener.setProperty('class', 'btn-danger')
		self.buttonGrabar = QPushButton('Grabar')
		self.buttonGrabar.setProperty('class', 'btn-success')
		self.buttonHistorial = QPushButton('Historial')
		self.buttonReportes = QPushButton('Reportes')
		self.buttonReportes.setProperty('class', 'btn-info')
		
		# self.buttonsGrid.addWidget(self.buttonRegistrar, 0, 0)
		self.buttonsGrid.addWidget(self.buttonIniciar, 1, 0)
		self.buttonsGrid.addWidget(self.buttonPausar, 1, 1)
		self.buttonsGrid.addWidget(self.buttonDetener, 1, 2)
		self.buttonsGrid.addWidget(self.buttonGrabar, 2, 0)
		self.buttonsGrid.addWidget(self.buttonHistorial, 2, 1)
		self.buttonsGrid.addWidget(self.buttonReportes, 2, 2)
		
		##right container
		# self.rightContainer.addLayout()
		self.rightContainer.addWidget( self.image_label )
		self.rightContainer.addWidget( QLabel('Webcam'))
		
		self.container.addLayout(topContainer)
		self.container.addLayout(colsContainer)
		self.setLayout( self.container )
		#self.setCentralLayout( self.container )
		
		video_image_label = self.video_image_label
		image_label = self.image_label
		window = self
		
		self.set_events()

	def build_objects_counter(self):
		box = QVBoxLayout()
		box.addWidget(QLabel('Diferenciación y conteo de los objetos'))
		hbox = QHBoxLayout()
		
		boxPerson = QVBoxLayout()
		pixmapPerson = QPixmap('{0}/images/person-icon.png'.format(config.BASE_DIR))
		labelPixmapPerson = QLabel('')
		labelPixmapPerson.setPixmap(pixmapPerson.scaled(QSize(60, 60), Qt.AspectRatioMode.KeepAspectRatio))
		# labelPixmapPerson.resize(90, 90)
		self.labelPersonCount = QLabel('0')
		self.labelPersonCount.setAlignment(Qt.AlignmentFlag.AlignCenter)
		boxPerson.addWidget(labelPixmapPerson)
		boxPerson.addWidget(self.labelPersonCount)
		hbox.addLayout(boxPerson)
		
		boxCar = QVBoxLayout()
		pixmapCar = QPixmap('{0}/images/car-icon.png'.format(config.BASE_DIR))
		labelPixmapCar = QLabel('')
		labelPixmapCar.setPixmap(pixmapCar.scaled(QSize(60, 60), Qt.AspectRatioMode.KeepAspectRatio))
		self.labelCarCount = QLabel('0')
		self.labelCarCount.setAlignment(Qt.AlignmentFlag.AlignCenter)
		boxCar.addWidget( labelPixmapCar )
		boxCar.addWidget(self.labelCarCount)
		hbox.addLayout(boxCar)
		
		boxMC = QVBoxLayout()
		pixmapMC = QPixmap('{0}/images/motorcicle.png'.format(config.BASE_DIR))
		labelPixmapMC = QLabel('')
		labelPixmapMC.setPixmap(pixmapMC.scaled(QSize(60, 60), Qt.AspectRatioMode.KeepAspectRatio))
		self.labelMCCount = QLabel('0')
		self.labelMCCount.setAlignment(Qt.AlignmentFlag.AlignCenter)
		boxMC.addWidget( labelPixmapMC )
		boxMC.addWidget(self.labelMCCount)
		hbox.addLayout(boxMC)
		
		boxAnimal = QVBoxLayout()
		pixmapAnimal = QPixmap('{0}/images/animal-icon.png'.format(config.BASE_DIR))
		labelPixmapAnimal = QLabel('')
		labelPixmapAnimal.setPixmap(pixmapAnimal.scaled(QSize(60, 60), Qt.AspectRatioMode.KeepAspectRatio))
		self.labelAnimalCount = QLabel('0')
		self.labelAnimalCount.setAlignment(Qt.AlignmentFlag.AlignCenter)
		boxAnimal.addWidget( labelPixmapAnimal )
		boxAnimal.addWidget(self.labelAnimalCount)
		hbox.addLayout(boxAnimal)
		
		
		
		box.addLayout(hbox)
		
		return box
		
	def set_events(self):
		self.buttonIniciar.clicked.connect(self.onBtnIniciarClicked)
	
	def get_video_image_label(self):
		return self.video_image_label
	
	def get_image_label(self):
		return self.image_label
		
	def onBtnIniciarClicked(self):
		self.startCapture()
		
	def startCapture(self):
		print('Starting capture thread')
		# start capture thread
		self.thread = VideoThread()
		self.thread.change_pixmap_signal.connect(update_video)
		self.thread.object_detected_signal.connect(update_image)
		self.thread.start()
		
	def set_user(self, user):
		
		self.current_user = user
		print(self.current_user)

	def set_counter(self, objType: str):
		# print('Setting counter for', objType)
		
		if objType in ['persona']:
			count = int(self.labelPersonCount.text())
			count += 1
			self.labelPersonCount.setText(str(count).zfill(6))
		elif objType in ['pajaro', 'gato', 'vaca', 'perro', 'caballo']:
			count = int(self.labelAnimalCount.text())
			count += 1
			self.labelAnimalCount.setText( str(count).zfill(6) )
		elif objType in ['bicicleta', 'motorbike']
			count = int(self.labelMCCount.text())
			count += 1
			self.labelMCCount.setText( str(count).zfill(6) )
		elif objType in ['automovil', 'bus']:
			count = int( self.labelCarCount.text() )
			count += 1
			self.labelCarCount.setText( str(count).zfill(6) )
