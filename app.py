# -*- coding: utf-8 -*-
import sys, os, time
from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QUrl
from PyQt6.QtMultimedia import QSoundEffect, QAudioOutput, QMediaPlayer
import simpleaudio as sa

import cv2
import numpy as np

import config
import database
from models.model_detector import ObjDetector
from main_window import MainWindow
from modals.login import LoginDialog

app = None
window = None
mwin = None

def start_database():
	database.create_new_session()
	from entities.user import User
	from entities.record_history import RecordHistory
	
	database.init_database()
	
def show_main_window(user):
	global window, mwin
	
	# print(user.username)
	
	window.close()
	mwin = MainWindow()
	mwin.set_user(user)
	mwin.show()
	
if __name__ == '__main__':
	os.environ['TZ'] = 'America/La_Paz'
	time.tzset()
	start_database()
	app = QApplication([])
	
	with open('{0}/css/style.css'.format(config.BASE_DIR)) as f:
		app.setStyleSheet(f.read())
	
	# window = MainWindow()
	window = LoginDialog()
	window.on_login_done.connect(show_main_window)
	'''
	window = QWidget()
	window.setWindowTitle('Detector de Objetos')

	leftContainer = QVBoxLayout()
	leftContainer.addWidget( QPushButton('Left Button') )

	rightContainer = QVBoxLayout()
	rightContainer.addWidget( QPushButton('Right Button') )

	container = QHBoxLayout()

	container.addLayout(leftContainer)
	container.addLayout(rightContainer)

	window.setLayout( container )

	video_image_label = QLabel()
	video_image_label.resize(300, 300)

	image_label = QLabel()
	image_label.resize(300, 300)

	leftContainer.addWidget( video_image_label )
	leftContainer.addWidget( QLabel('Live Video') )

	rightContainer.addWidget( image_label )
	rightContainer.addWidget( QLabel('Webcam'))

	# start capture thread
	thread = VideoThread()
	thread.change_pixmap_signal.connect(update_video)
	thread.object_detected_signal.connect(update_image)
	thread.start()
	'''
	window.show()

	# 5. Run your application's event loop
	sys.exit(app.exec())

