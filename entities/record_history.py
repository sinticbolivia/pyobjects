from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, orm
import database
from .base import BaseEntity

class RecordHistory(database.Base, BaseEntity):
	__tablename__	= 'recording_history'
	__table_args__	= {'sqlite_autoincrement': True} 
	
	id 				= Column(Integer, primary_key=True)
	user_id			= Column(Integer)
	name			= Column(String(128))
	border_post		= Column(String(128))
	lat				= Column(String(128))
	lng				= Column(String(128))
	start_datetime	= Column(DateTime, default=datetime.utcnow)
	end_datetime	= Column(DateTime)
	
	_serializable = ['id', 'user_id']
	
	def __init__(self):
		BaseEntity.__init__(self)
