from sqlalchemy import Column, String, Integer, create_engine, ForeignKey,Date,Time
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100),unique=True,nullable=False)
    password=Column(String(50),nullable=False)
    name=Column(String(100),nullable=False)
    gender=Column(String(2),nullable=False)
    dob=Column(Date,nullable=False)
    type = Column(String(20),nullable=False)
    Age = Column(Integer,nullable=False)

class Trek(Base):
    __tablename__="trek"

    id = Column(Integer, primary_key=True)
    name  = Column(String(100),unique=True,nullable=False)
    for_age_group=Column(Integer,nullable=True)
    no_of_slots=Column(Integer , nullable=False)
    no_of_registration = Column(Integer,default=0)
    trek_status = Column(String(20),nullable=False)
    difficulty = Column(String(10),nullable=False)
    start_date = Column( Date , nullable=False)
    end_date = Column(Date, nullable= False)
    disciption = Column(String(2000),nullable=True)
    starting_location = Column(String(100),nullable=False)
    ending_location = Column(String(100),nullable=False)
    registration_status = Column(String(100),nullable=False,default="open")

class deleted_items(Base):
    __tablename__="deleted_items"

    id = Column(Integer,primary_key=True)
    from_table= Column(String(20),nullable=False)
    id_of_deletd_item_from_the_table = Column(String(20),nullable=False)
    
class User_terk(Base):
    __tablename__='user_trek'
    registartion_id=Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    trek_id = Column(Integer, ForeignKey('trek.id'),nullable=False)
    completion = Column(String(20),nullable=False)
    payment_status = Column ( String(20) ,nullable= False)

class Staff_trek(Base):
    __tablename__='staff_trek'
    assign_id=Column(Integer, primary_key=True)
    trek_id = Column(Integer,ForeignKey("trek.id"),nullable=False)
    staff_id = Column(Integer,ForeignKey("users.id"),nullable=False)

def create_db():
    engine = create_engine("sqlite:///Database/trekking.db")
    Base.metadata.create_all(engine)
    print("db and tables are created")
