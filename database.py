from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import config

# engine = create_engine('sqlite:///db/{0}'.format(config.DB_NAME), connect_args={'check_same_thread': False})
# Session = sessionmaker(bind=engine)
# session = Session()
Base = declarative_base()
engine = None
session = None
# Base = None

def create_new_session():
	global engine, session, Base
	
	db_dir = '{0}/db'.format(config.BASE_DIR)
	if os.path.exists(db_dir ) == False:
		os.mkdir( db_dir )
	
	engine = create_engine('sqlite:///db/{0}'.format(config.DB_NAME), 
		connect_args={'check_same_thread': False}
	)
	Session = sessionmaker(bind=engine)
	session = Session()
	# Base = declarative_base()
	
	return session

def init_database():
	Base.metadata.create_all(engine)
	print('Base de datos inicializada con exito!!!')
