from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Formato: mysql+pymysql://usuario:contraseña@host:puerto/nombre_basedatos
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:admincl16@localhost:3306/productos_api"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()