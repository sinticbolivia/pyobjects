import json
from datetime import datetime 
from sqlalchemy import Column, Integer, String, Float, DateTime
# from sqlalchemy.orm import DeclarativeBase
import database
# print('BaseEntity', db)

class BaseEntity:
	# __tablename__ = ''
	# deleted					= Column(db.SmallInteger, default=0)
	# last_modification_date 	= Column(db.DateTime, default=datetime.utcnow)
	# creation_date			= Column(db.DateTime, default=datetime.utcnow)
	last_modification_date 	= Column(DateTime, default=datetime.now)
	creation_date			= Column(DateTime, default=datetime.now)
	
	_serializable	= []
	
	def __init__(self):
		pass
		#self._serializable	= []
	
	def bind(self, data):
		
		for key in data:
			setattr(self, key, data[key])
	
	def dict(self):
		data = {}
		print('_serializable', self._serializable)
		for attr in self._serializable:
			if attr[0] == '_':
				continue
			obj_attr = getattr(self, attr)
			if callable( obj_attr ):
				continue
			if str(type(obj_attr)) == "<type 'classobj'>" and callable(obj_attr, 'json'):
				data[attr] = obj_attr.json()
			else:
				data[attr] = getattr(self, attr)
			
		return data
		
	def json(self):
		return json.dumps(self.dict())
		
	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, 
			sort_keys=True, indent=4)
		
