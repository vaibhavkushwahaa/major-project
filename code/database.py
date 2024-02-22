from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column,Integer,String, DateTime
from datetime import datetime
from sqlalchemy.orm import sessionmaker

#base model class

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50),nullable=False)
    email = Column(String(50),unique=True)
    password = Column(String(50))
    created_at = Column(DateTime,default=datetime.now())

    def __str__(self):
        return self.username
    

#more classses for other tables
    
def open_db():
    engine= create_engine('sqlite:///project.db',echo=True)
    session=sessionmaker(bind=engine)
    return session()

def add_to_db(obj):
    db=open_db()
    db.add(obj)
    db.commit()
    db.close()



if __name__ == '__main__':
    #create engine
    #mysql setings
    # database_name= 'projectdb'
    # host = 'localhost'
    # username = 'root' #personal
    # password = 'root' #personal
    # port = 3306
    # engine= create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}',echo=True)
    
    #sqlite settings
    engine= create_engine('sqlite:///project.db',echo=True)
    Base.metadata.create_all(engine)

    

