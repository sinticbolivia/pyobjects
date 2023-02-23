# -*- coding: utf-8 -*-
import sys
from datetime import datetime

from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QTableView, QHeaderView, QSizePolicy)
from PyQt6.QtGui import QPixmap, QImage, QPixmap, QStandardItemModel
from PyQt6.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QUrl, QSize, QAbstractTableModel

import sqlalchemy

import database
from entities.record_history import RecordHistory
from entities.user import User

class RecordHistoryModel(QAbstractTableModel):
	
	def __init__(self, data):
		# super().__init__()
		super(RecordHistoryModel, self).__init__()
		self._data = data
		
		
	def rowCount(self, index):
		# The length of the outer list.
		return len(self._data)

	def columnCount(self, index):
		# The following takes the first sub-list, and returns
		# the length (only works if all rows are an equal length)
		return len(self._data[0])

		
	def data(self, index, role):
		
		if role == Qt.ItemDataRole.DisplayRole:
			_value = self._data[index.row()][index.column()]
			
			if isinstance(_value, datetime):
				return _value.strftime('%Y-%m-%d %H:%M:%S')
				
			return _value
	
class RecordHistoryDialog(QWidget):

	def __init__(self):
		super().__init__()
		self.setWindowTitle('Registro de Grabaciones')
		self.table_view = None
		self.build()
	
	def build(self):
		
		data = self._queryData()
		self.table_model = RecordHistoryModel(data)
		
		self.table_view = QTableView()
		self.table_view.setModel(self.table_model)
		
		self.container = QVBoxLayout()
		# self.container.addStretch(1)
		self.container.addWidget( self.table_view )
		self.setLayout(self.container)
		
		self._setTableHeaders()
		
		# self.setCentralWidget(self.table_view)
	
	def _setTableHeaders(self):
		headers = [
			'Usuario', 'Total Personas', 'Total Automoviles', 'Total Motocicletas', 
			'Total Animales', 'Fecha Creacion'
		]
		
		headmodel = QStandardItemModel()
		headmodel.setHorizontalHeaderLabels(headers)
		
		headview1 = QHeaderView(Qt.Orientation.Horizontal)
		headview1.setModel(headmodel)
		headview1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed) 
		
		self.table_view.setHorizontalHeader(headview1)

	def _queryData(self):
		query = database.session.query(
			#RecordHistory.user_id,
			User.username,
			RecordHistory.total_persons,
			#func.sum(RecordHistory.total_persons).label('total_persons'),
			RecordHistory.total_cars,
			RecordHistory.total_motorcicles,
			RecordHistory.total_animals,
			RecordHistory.creation_date,
		).filter(User.id == RecordHistory.user_id)
		#query = query.filter(payment.c.payment_date > '2005-05-25')
		# items = query.group_by( cast(RecordHistory.creation_date, Date) ).all()
		items = query.order_by( sqlalchemy.desc(RecordHistory.creation_date) ).all()
		
		return items
		
