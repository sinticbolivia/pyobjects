# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QLineEdit)
from PyQt6.QtGui import QPixmap, QImage, QPixmap
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QUrl, QSize

import config
from models.model_users import ModelUsers
from entities.user import User


class RecordDataDialog(QWidget):
	
	on_save = pyqtSignal(RecordDataDialog)
	
	def __init__(self):
		super().__init__()
		self.setWindowTitle('Datos de la Grabación')
		self.container = None
		self.labelName = None
		self.labelBorderPost = None
		self.inputName = None
		self.inputBorderPost = None
		self.buttonCancel = None
		self.buttonSave = None
		
	def build(self):
		self.container = QVBoxLayout()
		self.labelName = QLabel('Nombre de la Grabacion')
		self.labelBorderPost = QLabel('Nombre del puesto fronterizo')
		self.inputName = QLineEdit(self)
		self.inputBorderPost = QLineEdit(self)
		self.buttonCancel = QPushButton('Cancelar')
		self.buttonSave = QPushButton('Guardar')
		
		boxButtons = QHBoxLayout()
		boxButtons.addWidget(self.buttonCancel)
		boxButtons.addWidget(self.buttonSave)
		
		self.container.addWidget(self.labelName)
		self.container.addWidget(self.inputName)
		self.container.addWidget(self.labelBorderPost)
		self.container.addWidget(self.inputBorderPost)
		self.container.addLayout(boxButtons)
		self.container.addStretch()
		
		self.setLayout( self.container )
		self.set_events()
		
	def set_events(self):
		self.buttonCancel.clicked.connect(self.onButtonCancelClicked)
		self.buttonSave.clicked.connect(self.onButtonSaveClicked)
		
	def onButtonCancelClicked(self):
		pass
		
	def onButtonSaveClicked(self):
		
		self.on_save.emit(self)
