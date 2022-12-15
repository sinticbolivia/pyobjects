import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, orm, event
#from noconflict import classmaker
import database
from .base import BaseEntity
import hashlib

class User(database.Base, BaseEntity):
	##__metaclass__	= BaseEntity
	__tablename__	= 'users'
	__table_args__	= {'sqlite_autoincrement': True} 
	
	id 				= Column(Integer, primary_key=True)
	firstname		= Column(String(128))
	lastname		= Column(String(128))
	email			= Column(String(128))
	username		= Column(String(128))
	pwd				= Column(String(128))
	document_num	= Column(String(64))
	phone			= Column(String(64))
	# creation_date	= Column(DateTime, default=datetime.datetime.utcnow)
	
	_serializable = ['id', 'name', 'document_num', 'certificate']
	
	def __init__(self):
		BaseEntity.__init__(self)
		# super().__init__()

	#@orm.reconstructor
	#def init_on_load(self):
	#	self._serializable = ['id', 'name', 'document_num', 'certificate']

def populate_data(target, connection, **kw):
	connection.execute(target.insert(), {'firstname': 'root', 'lastname': 'root', 'email': '', 'username': 'root', 'pwd': hashlib.md5('root'.encode()).hexdigest()})
	 
event.listen(User.__table__, 'after_create', populate_data)
