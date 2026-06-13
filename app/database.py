from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

password = quote_plus("password123")

#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<databse_name>' - the basic format of the url
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{password}@localhost/fastapi" #databse connection url using sqlalchemy

engine = create_engine(SQLALCHEMY_DATABASE_URL) #responsible for the connection between sqlalchemy and postgres

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #to interact with the databse we use a session

Base = declarative_base() #all of the defined models will extend this base class

def get_db(): #the session object is responsible to connect to databse, so every request gets us a new session, we can send sql statements to it, and after we're done finally it closes the session
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()