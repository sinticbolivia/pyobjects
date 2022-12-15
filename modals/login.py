# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QLineEdit)
from PyQt6.QtGui import QPixmap, QImage, QPixmap
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QUrl, QSize

import config
from models.model_users import ModelUsers
from entities.user import User

class LoginDialog(QWidget):

	on_login_done = pyqtSignal(User)
	
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Ingreso al Sistema')
		self.container 		= None
		self.buttonLogin 	= None
		self.inputUsername 	= None
		self.inputPasword	= None
		
		self.build()

	def build(self):
		self.inputUsername = QLineEdit(self)
		self.inputPassword = QLineEdit(self)
		self.inputPassword.setEchoMode(QLineEdit.EchoMode.Password)
		
		self.buttonLogin	= QPushButton('Iniciar sesión')
		self.buttonLogin.setProperty('class', 'btn-primary')
		
		self.container = QVBoxLayout()
		self.container.addStretch(1)
		pixmapLogo = QPixmap('{0}/images/EjercitoEB.png'.format(config.BASE_DIR))
		labelPixmapLogo = QLabel('')
		labelPixmapLogo.setPixmap(pixmapLogo.scaled(QSize(100, 100), Qt.AspectRatioMode.KeepAspectRatio))
		labelPixmapLogo.setAlignment(Qt.AlignmentFlag.AlignCenter)
		
		labelTitle = QLabel('Inicio de Sesión')
		labelTitle.setProperty('class', ['title', 'text-center'])
		# labelTitle.setStyleSheet('QLabel{background-color:red;text-align:center;}')
		labelTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
		
		self.container.addWidget( labelPixmapLogo )
		self.container.addWidget( labelTitle )
		self.container.addWidget( QLabel('Usuario') )
		self.container.addWidget( self.inputUsername )
		self.container.addWidget( QLabel('Contraseña') )
		self.container.addWidget( self.inputPassword )
		self.container.addWidget( self.buttonLogin )
		self.container.addStretch(1)
		self.setLayout(self.container)
		
		self.set_events()
		
	def set_events(self):
		
		self.buttonLogin.clicked.connect( self.onButtonLoginClicked )
		
	def onButtonLoginClicked(self):
		username = self.inputUsername.text().strip()
		password = self.inputPassword.text().strip()
		model = ModelUsers()
		
		try:
			user = model.login(username, password)
			self.on_login_done.emit(user)
			
		except Exception as e:
			print('ERROR', e)
