from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
import psycopg2
import time
from psycopg2.extras import RealDictCursor
from .config import settings 

password = quote_plus("password123")

#SQLALCHEMY_DATABASE_URL = f'postgresql://<username>:<password>@<ip-address/hostname>/<databse_name>' - the basic format of the url
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}" #databse connection url using sqlalchemy

engine = create_engine(SQLALCHEMY_DATABASE_URL) #responsible for the connection between sqlalchemy and postgres

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #to interact with the databse we use a session

Base = declarative_base() #all of the defined models will extend this base class

def get_db(): #the session object is responsible to connect to databse, so every request gets us a new session, we can send sql statements to it, and after we're done finally it closes the session
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

while True:  #to continue trying to connect to the databse until successful

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='password123',cursor_factory=RealDictCursor) #establishing a connection to the database
        cursor = conn.cursor()  #cursor is used to execute the commands
        print("Database connection was succesfull!!")
        break

    except Exception as error:
        print("Connecting to database failed")    #except the error if connection failed
        print("Error: ", error)
        time.sleep(3)
 