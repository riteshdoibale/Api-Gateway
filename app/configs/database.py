from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.configs.config import db_protocol, db_diletics, db_username, db_password, db_url, db_port,db_name

engine = None
database_connection_sesion = None
Base = None
session = None

class DatabaseConnection(object):
    
    protocol = db_protocol
    diletics = db_diletics
    username = db_username
    password = db_password
    url = db_url
    port = db_port
    name = db_name
    
    def __init__(self):
        pass
    
    def get_database_url(self):
        
        database_url = self.protocol + "+" + self.diletics + "://" + self.username + ":" + self.password + "@" + self.url + ":" + str(
            self.port) + "/" + self.name
        return database_url
    
    @classmethod
    def establish_db_connection(self):
        try:
            global engine
            global database_connection_sesion
            global Base
            global session
            
            engine = create_engine(self.get_database_url(self))
            
            session = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
            
            Base = declarative_base()
            print("database connection establish successfully")
        except Exception as e:
            print(e)
        return True
    
    @classmethod
    def get_db_connection(self):
        database_connection_sesion = session()
        try:
            return database_connection_sesion
        except Exception as e:
            database_connection_sesion.rollback()
            raise
        finally:
            database_connection_sesion.close()