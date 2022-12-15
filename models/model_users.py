import hashlib

import database
from entities.user import User

class ModelUsers:

	def __init__(self):
		pass
		
	def login(self, username, pwd):
		record = database.session.query(User).filter_by(username=username).first()
		if record is None:
			raise Exception('El usuario no existe')
			
		pwd_md5 = hashlib.md5(pwd.encode()).hexdigest()
		# print(record)
		
		if pwd_md5 != record.pwd:
			raise Exception('Nombre de usuario o contraseña invalida')
		
		return record
		
